"""
Resume API Routes
Endpoints for resume upload, analysis, and retrieval
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from typing import Optional
from datetime import datetime
from bson import ObjectId

from app.schemas.resume import ResumeAnalysisResponse
from app.schemas.response import SuccessResponse
from app.services.resume_parser import resume_parser
from app.services.ats_scorer import ats_scorer
from app.services.skill_extractor import skill_extractor
from app.utils.file_handler import FileHandler
from app.database.connection import get_database
from app.core.logging import get_logger
from app.core.exceptions import (
    FileProcessingError,
    InvalidFileTypeError,
    FileSizeExceededError,
    ResumeParsingError
)

logger = get_logger(__name__)
router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", response_model=dict, status_code=201)
async def upload_and_analyze_resume(
    file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_role: Optional[str] = Form(None),
    job_description: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    db=Depends(get_database)
):
    """
    Upload and analyze a resume
    
    - **file**: Resume file (PDF or DOCX, max 5MB)
    - **job_role**: Target job role for tailored analysis
    - **job_description**: Optional job description for ATS scoring
    - **user_id**: Optional user identifier
    """
    try:
        logger.info(f"Received resume upload: {file.filename}")
        
        # Read file content
        file_content = await file.read()
        
        # Save file
        file_handler = FileHandler()
        file_path, unique_filename = await file_handler.save_upload_file(
            file_content,
            file.filename,
            user_id
        )
        
        # Extract text from resume
        resume_text = file_handler.extract_text(file_path)
        
        # Parse resume
        parsed_data = resume_parser.parse(resume_text)
        
        # Calculate ATS score
        ats_score_result = ats_scorer.calculate_ats_score(
            resume_text=resume_text,
            parsed_data=parsed_data,
            job_description=job_description,
            target_role=job_role
        )
        
        # Get job role recommendations
        skills = parsed_data.get("skills", {}).get("all_skills", [])
        recommended_roles = skill_extractor.recommend_job_roles(skills, top_n=5)
        
        # Prepare document for MongoDB
        resume_document = {
            "user_id": user_id,
            "file_name": file.filename,
            "unique_file_name": unique_filename,
            "file_path": file_path,
            "upload_date": datetime.utcnow(),
            "job_role": job_role,
            "parsed_data": parsed_data,
            "ats_score": ats_score_result,
            "recommended_roles": recommended_roles,
            "status": "analyzed"
        }
        
        # Save to database
        result = await db.resumes.insert_one(resume_document)
        resume_id = str(result.inserted_id)
        
        logger.info(f"Resume analyzed successfully: {resume_id}")
        
        # Prepare response
        return {
            "success": True,
            "message": "Resume analyzed successfully",
            "data": {
                "resume_id": resume_id,
                "file_name": file.filename,
                "upload_date": resume_document["upload_date"].isoformat(),
                "parsed_data": parsed_data,
                "ats_score": ats_score_result,
                "recommended_roles": recommended_roles
            }
        }
        
    except (InvalidFileTypeError, FileSizeExceededError, FileProcessingError, ResumeParsingError) as e:
        logger.error(f"Resume processing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during resume upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{resume_id}", response_model=dict)
async def get_resume_analysis(
    resume_id: str,
    db=Depends(get_database)
):
    """
    Get resume analysis by ID
    
    - **resume_id**: Resume document ID
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(resume_id):
            raise HTTPException(status_code=400, detail="Invalid resume ID")
        
        # Fetch from database
        resume = await db.resumes.find_one({"_id": ObjectId(resume_id)})
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Convert ObjectId to string
        resume["_id"] = str(resume["_id"])
        resume["resume_id"] = resume.pop("_id")
        
        # Convert date to ISO format
        if "upload_date" in resume:
            resume["upload_date"] = resume["upload_date"].isoformat()
        
        return {
            "success": True,
            "data": resume
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving resume: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/user/{user_id}", response_model=dict)
async def get_user_resumes(
    user_id: str,
    limit: int = 10,
    skip: int = 0,
    db=Depends(get_database)
):
    """
    Get all resumes for a user
    
    - **user_id**: User identifier
    - **limit**: Maximum number of results
    - **skip**: Number of results to skip
    """
    try:
        # Query database
        cursor = db.resumes.find(
            {"user_id": user_id}
        ).sort("upload_date", -1).skip(skip).limit(limit)
        
        resumes = await cursor.to_list(length=limit)
        
        # Count total
        total = await db.resumes.count_documents({"user_id": user_id})
        
        # Format results
        result_list = []
        for resume in resumes:
            result_list.append({
                "resume_id": str(resume["_id"]),
                "file_name": resume.get("file_name"),
                "upload_date": resume.get("upload_date").isoformat(),
                "overall_score": resume.get("ats_score", {}).get("overall_score", 0),
                "job_role": resume.get("job_role"),
                "status": resume.get("status", "analyzed")
            })
        
        return {
            "success": True,
            "data": {
                "resumes": result_list,
                "total": total,
                "limit": limit,
                "skip": skip
            }
        }
        
    except Exception as e:
        logger.error(f"Error retrieving user resumes: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{resume_id}", response_model=SuccessResponse)
async def delete_resume(
    resume_id: str,
    db=Depends(get_database)
):
    """
    Delete a resume and its associated file
    
    - **resume_id**: Resume document ID
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(resume_id):
            raise HTTPException(status_code=400, detail="Invalid resume ID")
        
        # Get resume to find file path
        resume = await db.resumes.find_one({"_id": ObjectId(resume_id)})
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Delete file
        file_handler = FileHandler()
        if "file_path" in resume:
            file_handler.delete_file(resume["file_path"])
        
        # Delete from database
        await db.resumes.delete_one({"_id": ObjectId(resume_id)})
        
        logger.info(f"Resume deleted: {resume_id}")
        
        return SuccessResponse(
            success=True,
            message="Resume deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting resume: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
