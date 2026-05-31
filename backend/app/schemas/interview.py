"""
Interview-related Pydantic Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
from datetime import datetime


class QuestionRequest(BaseModel):
    """Request to generate interview questions"""
    job_role: str = Field(..., min_length=2, max_length=100)
    num_technical: int = Field(default=5, ge=1, le=10)
    num_hr: int = Field(default=3, ge=1, le=10)
    difficulty: Optional[str] = Field(default=None)
    
    @validator("difficulty")
    def validate_difficulty(cls, v):
        if v and v.lower() not in ["easy", "medium", "hard"]:
            raise ValueError("Difficulty must be easy, medium, or hard")
        return v.lower() if v else None
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_role": "Software Engineer",
                "num_technical": 5,
                "num_hr": 3,
                "difficulty": "medium"
            }
        }


class Question(BaseModel):
    """Interview question schema"""
    question_id: str
    question_type: str
    question_text: str
    difficulty: str
    category: str
    expected_keywords: List[str]
    max_time_seconds: int


class AnswerSubmission(BaseModel):
    """User's answer submission"""
    question_id: str
    answer_text: str = Field(..., min_length=1, max_length=5000)
    time_taken_seconds: Optional[int] = None
    
    @validator("answer_text")
    def validate_answer(cls, v):
        if not v.strip():
            raise ValueError("Answer cannot be empty")
        return v.strip()


class AnswerEvaluation(BaseModel):
    """Answer evaluation result"""
    overall_score: float
    score_percentage: float
    component_scores: Dict[str, float]
    analysis: Dict
    feedback: Dict
    grade: str


class InterviewStartRequest(BaseModel):
    """Request to start an interview"""
    user_id: Optional[str] = None
    job_role: str
    num_technical: int = Field(default=5)
    num_hr: int = Field(default=3)


class InterviewResponse(BaseModel):
    """Response after starting interview"""
    interview_id: str
    job_role: str
    questions: List[Question]
    total_questions: int
    estimated_duration_minutes: int


class InterviewSubmissionRequest(BaseModel):
    """Request to submit complete interview"""
    interview_id: str
    answers: List[Dict[str, any]]


class InterviewResultResponse(BaseModel):
    """Interview evaluation results"""
    interview_id: str
    job_role: str
    submitted_at: datetime
    overall_performance: Dict
    question_results: List[Dict]
    recommendations: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "interview_id": "507f1f77bcf86cd799439011",
                "job_role": "Software Engineer",
                "submitted_at": "2024-01-15T14:30:00",
                "overall_performance": {
                    "overall_score": 75.5,
                    "technical_score": 78.0,
                    "hr_score": 72.0
                },
                "question_results": [],
                "recommendations": ["Improve data structures knowledge"]
            }
        }


class InterviewListItem(BaseModel):
    """Interview list item for user dashboard"""
    interview_id: str
    job_role: str
    date: datetime
    overall_score: float
    status: str
