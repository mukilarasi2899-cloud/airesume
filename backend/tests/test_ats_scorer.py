import pytest
from app.services.ats_scorer import ATSScorer

@pytest.fixture
def ats_scorer():
    return ATSScorer()

@pytest.fixture
def sample_resume_dict():
    return {
        'skills': {
            'all_skills': ['Python', 'FastAPI', 'React', 'MongoDB', 'Docker'],
            'technical_skills': ['Python', 'FastAPI', 'React', 'MongoDB', 'Docker']
        },
        'experience': [
            {'title': 'Software Engineer', 'company': 'Tech Corp', 'duration': '3 years'}
        ],
        'education': [
            {'degree': 'Bachelor of Science', 'field': 'Computer Science'}
        ],
        'total_experience_years': 3
    }

def test_keyword_matching(ats_scorer, sample_resume_dict):
    """Test keyword matching against job description"""
    resume_text = "Python FastAPI React MongoDB Docker Software Engineer"
    job_desc = "Looking for Python developer with FastAPI and React experience"
    
    score = ats_scorer.calculate_ats_score(resume_text, sample_resume_dict, job_desc)
    assert score['component_scores']['keyword_match'] > 0

def test_tfidf_similarity(ats_scorer, sample_resume_dict):
    """Test TF-IDF similarity calculation"""
    resume_text = "Experienced Python developer with FastAPI and React skills"
    job_desc = "Python developer needed for web development with FastAPI"
    
    score = ats_scorer.calculate_ats_score(resume_text, sample_resume_dict, job_desc)
    assert score['component_scores']['tfidf_similarity'] > 0

def test_weighted_score(ats_scorer, sample_resume_dict):
    """Test overall weighted score calculation"""
    resume_text = "Python FastAPI React MongoDB"
    job_desc = "Python developer"
    
    score = ats_scorer.calculate_ats_score(resume_text, sample_resume_dict, job_desc)
    assert 0 <= score['overall_score'] <= 100
    assert 'score_interpretation' in score

def test_missing_keywords(ats_scorer, sample_resume_dict):
    """Test missing keyword identification"""
    resume_text = "Python React"
    job_desc = "Python React Kubernetes AWS Machine Learning"
    
    score = ats_scorer.calculate_ats_score(resume_text, sample_resume_dict, job_desc)
    assert len(score['analysis']['missing_keywords']) > 0

def test_improvement_suggestions(ats_scorer, sample_resume_dict):
    """Test improvement recommendations"""
    resume_text = "Basic Python experience"
    job_desc = "Senior Python developer with 5+ years experience"
    
    score = ats_scorer.calculate_ats_score(resume_text, sample_resume_dict, job_desc)
    assert len(score['analysis']['recommendations']) > 0
