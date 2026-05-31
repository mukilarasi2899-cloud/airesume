"""
Interview API Routes
Endpoints for mock interview functionality
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict
from datetime import datetime
from bson import ObjectId

from app.schemas.interview import (
    QuestionRequest,
    InterviewStartRequest,
    AnswerSubmission,
    InterviewResponse,
    InterviewResultResponse
)
from app.schemas.response import SuccessResponse
from app.services.question_generator import question_generator
from app.services.answer_evaluator import answer_evaluator
from app.database.connection import get_database
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/start", response_model=dict, status_code=201)
async def start_interview(
    request: InterviewStartRequest,
    db=Depends(get_database)
):
    """
    Start a new mock interview session
    
    - **job_role**: Target job role
    - **num_technical**: Number of technical questions
    - **num_hr**: Number of HR questions
    - **user_id**: Optional user identifier
    """
    try:
        logger.info(f"Starting interview for role: {request.job_role}")
        
        # Generate questions
        questions = question_generator.generate_interview_questions(
            job_role=request.job_role,
            num_technical=request.num_technical,
            num_hr=request.num_hr
        )
        
        # Calculate estimated duration
        total_time = sum(q["max_time_seconds"] for q in questions)
        estimated_minutes = round(total_time / 60)
        
        # Create interview document
        interview_document = {
            "user_id": request.user_id,
            "job_role": request.job_role,
            "status": "in_progress",
            "created_at": datetime.utcnow(),
            "questions": questions,
            "answers": [],
            "total_questions": len(questions),
            "estimated_duration_minutes": estimated_minutes
        }
        
        # Save to database
        result = await db.interviews.insert_one(interview_document)
        interview_id = str(result.inserted_id)
        
        logger.info(f"Interview started: {interview_id}")
        
        return {
            "success": True,
            "message": "Interview started successfully",
            "data": {
                "interview_id": interview_id,
                "job_role": request.job_role,
                "questions": questions,
                "total_questions": len(questions),
                "estimated_duration_minutes": estimated_minutes
            }
        }
        
    except Exception as e:
        logger.error(f"Error starting interview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{interview_id}/answer", response_model=dict)
async def submit_answer(
    interview_id: str,
    answer: AnswerSubmission,
    db=Depends(get_database)
):
    """
    Submit an answer to an interview question
    
    - **interview_id**: Interview session ID
    - **answer**: Answer submission with question_id and answer_text
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(interview_id):
            raise HTTPException(status_code=400, detail="Invalid interview ID")
        
        # Get interview
        interview = await db.interviews.find_one({"_id": ObjectId(interview_id)})
        
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        # Find the question
        question = None
        for q in interview["questions"]:
            if q["question_id"] == answer.question_id:
                question = q
                break
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Evaluate answer
        evaluation = answer_evaluator.evaluate_answer(
            user_answer=answer.answer_text,
            question=question
        )
        
        # Create answer record
        answer_record = {
            "question_id": answer.question_id,
            "question_text": question["question_text"],
            "question_type": question["question_type"],
            "user_answer": answer.answer_text,
            "time_taken_seconds": answer.time_taken_seconds,
            "evaluation": evaluation,
            "submitted_at": datetime.utcnow()
        }
        
        # Update interview with answer
        await db.interviews.update_one(
            {"_id": ObjectId(interview_id)},
            {"$push": {"answers": answer_record}}
        )
        
        logger.info(f"Answer submitted for interview {interview_id}, question {answer.question_id}")
        
        return {
            "success": True,
            "message": "Answer evaluated successfully",
            "data": {
                "question_id": answer.question_id,
                "evaluation": evaluation
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting answer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{interview_id}/complete", response_model=dict)
async def complete_interview(
    interview_id: str,
    db=Depends(get_database)
):
    """
    Complete an interview and get overall performance
    
    - **interview_id**: Interview session ID
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(interview_id):
            raise HTTPException(status_code=400, detail="Invalid interview ID")
        
        # Get interview
        interview = await db.interviews.find_one({"_id": ObjectId(interview_id)})
        
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        answers = interview.get("answers", [])
        
        if not answers:
            raise HTTPException(status_code=400, detail="No answers submitted")
        
        # Calculate overall performance
        overall_performance = answer_evaluator.evaluate_interview_performance(answers)
        
        # Generate recommendations
        recommendations = []
        
        if overall_performance["technical_score"] < 60:
            recommendations.append("Focus on strengthening technical fundamentals")
        
        if overall_performance["hr_score"] < 60:
            recommendations.append("Work on communication and behavioral interview skills")
        
        if overall_performance["overall_score"] < 70:
            recommendations.append("Practice more mock interviews to improve confidence")
        
        if overall_performance["overall_score"] >= 85:
            recommendations.append("Excellent performance! You're well-prepared for interviews")
        
        # Update interview status
        await db.interviews.update_one(
            {"_id": ObjectId(interview_id)},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": datetime.utcnow(),
                    "overall_performance": overall_performance,
                    "recommendations": recommendations
                }
            }
        )
        
        logger.info(f"Interview completed: {interview_id}")
        
        return {
            "success": True,
            "message": "Interview completed successfully",
            "data": {
                "interview_id": interview_id,
                "job_role": interview["job_role"],
                "completed_at": datetime.utcnow().isoformat(),
                "overall_performance": overall_performance,
                "total_questions": len(interview["questions"]),
                "answered_questions": len(answers),
                "recommendations": recommendations,
                "detailed_results": answers
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error completing interview: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{interview_id}", response_model=dict)
async def get_interview(
    interview_id: str,
    db=Depends(get_database)
):
    """
    Get interview details
    
    - **interview_id**: Interview session ID
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(interview_id):
            raise HTTPException(status_code=400, detail="Invalid interview ID")
        
        # Get interview
        interview = await db.interviews.find_one({"_id": ObjectId(interview_id)})
        
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        # Format response
        interview["_id"] = str(interview["_id"])
        interview["interview_id"] = interview.pop("_id")
        
        # Convert dates to ISO format
        for date_field in ["created_at", "completed_at"]:
            if date_field in interview and interview[date_field]:
                interview[date_field] = interview[date_field].isoformat()
        
        return {
            "success": True,
            "data": interview
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving interview: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/user/{user_id}", response_model=dict)
async def get_user_interviews(
    user_id: str,
    limit: int = 10,
    skip: int = 0,
    db=Depends(get_database)
):
    """
    Get all interviews for a user
    
    - **user_id**: User identifier
    - **limit**: Maximum number of results
    - **skip**: Number of results to skip
    """
    try:
        # Query database
        cursor = db.interviews.find(
            {"user_id": user_id}
        ).sort("created_at", -1).skip(skip).limit(limit)
        
        interviews = await cursor.to_list(length=limit)
        
        # Count total
        total = await db.interviews.count_documents({"user_id": user_id})
        
        # Format results
        result_list = []
        for interview in interviews:
            result_list.append({
                "interview_id": str(interview["_id"]),
                "job_role": interview.get("job_role"),
                "date": interview.get("created_at").isoformat(),
                "status": interview.get("status"),
                "overall_score": interview.get("overall_performance", {}).get("overall_score", 0),
                "total_questions": interview.get("total_questions", 0)
            })
        
        return {
            "success": True,
            "data": {
                "interviews": result_list,
                "total": total,
                "limit": limit,
                "skip": skip
            }
        }
        
    except Exception as e:
        logger.error(f"Error retrieving user interviews: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/roles/available", response_model=dict)
async def get_available_roles():
    """
    Get list of available job roles for interviews
    """
    try:
        roles = question_generator.get_available_roles()
        
        return {
            "success": True,
            "data": {
                "roles": roles,
                "total": len(roles)
            }
        }
        
    except Exception as e:
        logger.error(f"Error retrieving roles: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats/{interview_id}", response_model=dict)
async def get_interview_statistics(
    interview_id: str,
    db=Depends(get_database)
):
    """
    Get detailed statistics for an interview
    
    - **interview_id**: Interview session ID
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(interview_id):
            raise HTTPException(status_code=400, detail="Invalid interview ID")
        
        # Get interview
        interview = await db.interviews.find_one({"_id": ObjectId(interview_id)})
        
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        answers = interview.get("answers", [])
        
        # Calculate statistics
        stats = {
            "total_questions": len(interview.get("questions", [])),
            "answered_questions": len(answers),
            "average_score": sum(a["evaluation"]["overall_score"] for a in answers) / len(answers) if answers else 0,
            "technical_questions": len([a for a in answers if a["question_type"] == "technical"]),
            "hr_questions": len([a for a in answers if a["question_type"] == "hr"]),
            "category_performance": {},
            "difficulty_performance": {}
        }
        
        # Group by category
        for answer in answers:
            category = answer.get("question_type", "Unknown")
            if category not in stats["category_performance"]:
                stats["category_performance"][category] = {
                    "count": 0,
                    "average_score": 0,
                    "scores": []
                }
            stats["category_performance"][category]["count"] += 1
            stats["category_performance"][category]["scores"].append(
                answer["evaluation"]["overall_score"]
            )
        
        # Calculate averages for categories
        for category in stats["category_performance"]:
            scores = stats["category_performance"][category]["scores"]
            stats["category_performance"][category]["average_score"] = sum(scores) / len(scores)
            del stats["category_performance"][category]["scores"]
        
        return {
            "success": True,
            "data": stats
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving interview stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
