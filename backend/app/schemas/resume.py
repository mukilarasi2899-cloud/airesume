"""
Resume-related Pydantic Schemas
Request and response models for resume operations
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class ContactInfo(BaseModel):
    """Contact information schema"""
    emails: List[str] = Field(default_factory=list)
    phones: List[str] = Field(default_factory=list)
    urls: List[str] = Field(default_factory=list)
    linkedin: Optional[str] = None
    github: Optional[str] = None


class Education(BaseModel):
    """Education entry schema"""
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[int] = None
    field: Optional[str] = None


class Experience(BaseModel):
    """Work experience schema"""
    title: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    description: str = ""
    years: float = 0.0


class Project(BaseModel):
    """Project schema"""
    name: Optional[str] = None
    description: str = ""
    technologies: List[str] = Field(default_factory=list)


class Skills(BaseModel):
    """Skills schema"""
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    all_skills: List[str] = Field(default_factory=list)


class ATSScore(BaseModel):
    """ATS scoring schema"""
    overall_score: float
    keyword_match: float
    tfidf_similarity: float
    skill_match: float
    format_quality: float
    experience_score: float
    education_score: float


class Feedback(BaseModel):
    """Resume feedback schema"""
    weak_areas: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class ResumeUploadRequest(BaseModel):
    """Resume upload request"""
    job_role: Optional[str] = Field(None, description="Target job role for analysis")
    job_description: Optional[str] = Field(None, description="Optional job description")


class ParsedResumeData(BaseModel):
    """Parsed resume data schema"""
    contact_info: ContactInfo
    summary: str = ""
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    skills: Skills
    skill_clusters: Dict[str, List[str]] = Field(default_factory=dict)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    total_experience_years: float = 0.0
    language_quality: Dict = Field(default_factory=dict)
    parsing_metadata: Dict = Field(default_factory=dict)


class ResumeAnalysisResponse(BaseModel):
    """Resume analysis response"""
    resume_id: str
    file_name: str
    upload_date: datetime
    parsed_data: ParsedResumeData
    ats_score: Dict
    feedback: Feedback
    recommended_roles: List[Dict] = Field(default_factory=list)


class ResumeListItem(BaseModel):
    """Resume list item for user dashboard"""
    resume_id: str
    file_name: str
    upload_date: datetime
    overall_score: float
    job_role: Optional[str] = None


class ResumeListResponse(BaseModel):
    """Resume list response"""
    resumes: List[ResumeListItem]
    total: int
