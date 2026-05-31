import pytest
from app.services.resume_parser import ResumeParser

@pytest.fixture
def resume_parser():
    return ResumeParser()

@pytest.fixture
def sample_resume_text():
    return """
    John Doe
    john.doe@email.com | +1-234-567-8900
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology, 2020
    GPA: 3.8/4.0
    
    EXPERIENCE
    Software Engineer - Tech Corp (2020-2023)
    - Developed web applications using Python and React
    - Improved system performance by 40%
    
    SKILLS
    Python, JavaScript, React, FastAPI, MongoDB, Docker
    
    PROJECTS
    E-commerce Platform - Built full-stack application
    """

def test_parse_education(resume_parser, sample_resume_text):
    """Test education extraction"""
    result = resume_parser.parse_resume(sample_resume_text)
    assert len(result['education']) > 0
    assert 'Bachelor' in str(result['education'])

def test_extract_skills(resume_parser, sample_resume_text):
    """Test skill extraction"""
    result = resume_parser.parse_resume(sample_resume_text)
    skills = result['skills']['all_skills']
    assert 'Python' in skills
    assert 'React' in skills
    assert 'FastAPI' in skills

def test_extract_experience(resume_parser, sample_resume_text):
    """Test experience extraction"""
    result = resume_parser.parse_resume(sample_resume_text)
    assert len(result['experience']) > 0
    assert result['total_experience_years'] > 0

def test_extract_contact_info(resume_parser, sample_resume_text):
    """Test contact information extraction"""
    result = resume_parser.parse_resume(sample_resume_text)
    assert result['contact_info']['email'] == 'john.doe@email.com'
    assert result['contact_info']['phone'] == '+1-234-567-8900'

def test_extract_projects(resume_parser, sample_resume_text):
    """Test project extraction"""
    result = resume_parser.parse_resume(sample_resume_text)
    assert len(result['projects']) > 0
