import pytest
from app.services.question_generator import QuestionGenerator
from app.services.answer_evaluator import AnswerEvaluator

@pytest.fixture
def question_generator():
    return QuestionGenerator()

@pytest.fixture
def answer_evaluator():
    return AnswerEvaluator()

def test_question_generation(question_generator):
    """Test interview question generation"""
    questions = question_generator.generate_interview_questions(
        job_role='software_engineer',
        num_technical=5,
        num_hr=3
    )
    
    assert len(questions) == 8
    assert all('question_text' in q for q in questions)
    assert all('difficulty' in q for q in questions)

def test_question_difficulty_levels(question_generator):
    """Test different difficulty levels"""
    easy_questions = question_generator.generate_interview_questions(
        job_role='software_engineer',
        num_technical=3,
        difficulty='easy'
    )
    
    assert all(q['difficulty'] == 'easy' for q in easy_questions if q['question_type'] == 'technical')

def test_answer_evaluation(answer_evaluator):
    """Test answer evaluation"""
    question = {
        'question_text': 'Explain object-oriented programming',
        'keywords': ['encapsulation', 'inheritance', 'polymorphism', 'abstraction'],
        'category': 'Programming Concepts'
    }
    
    answer = """
    Object-oriented programming is a paradigm that uses objects and classes.
    It has four main principles: encapsulation, inheritance, polymorphism, and abstraction.
    Encapsulation bundles data and methods. Inheritance allows code reuse.
    Polymorphism enables objects to take multiple forms. Abstraction hides complexity.
    """
    
    evaluation = answer_evaluator.evaluate_answer(question, answer)
    
    assert 0 <= evaluation['overall_score'] <= 100
    assert 'keyword_coverage' in evaluation['component_scores']
    assert 'semantic_similarity' in evaluation['component_scores']

def test_keyword_coverage(answer_evaluator):
    """Test keyword coverage in answers"""
    question = {
        'question_text': 'What is REST API?',
        'keywords': ['HTTP', 'GET', 'POST', 'stateless', 'resource'],
        'category': 'Web Development'
    }
    
    answer = "REST API uses HTTP methods like GET and POST for stateless resource manipulation"
    
    evaluation = answer_evaluator.evaluate_answer(question, answer)
    assert evaluation['component_scores']['keyword_coverage'] > 50

def test_empty_answer(answer_evaluator):
    """Test handling of empty answers"""
    question = {
        'question_text': 'Explain databases',
        'keywords': ['data', 'storage', 'query'],
        'category': 'Database'
    }
    
    evaluation = answer_evaluator.evaluate_answer(question, "")
    assert evaluation['overall_score'] == 0

def test_hr_question_evaluation(answer_evaluator):
    """Test HR question evaluation with STAR method"""
    question = {
        'question_text': 'Describe a challenging project',
        'keywords': ['challenge', 'solution', 'result'],
        'category': 'Behavioral',
        'question_type': 'hr'
    }
    
    answer = """
    In my previous role, we faced a challenging deadline (Situation).
    I was tasked with optimizing the system (Task).
    I analyzed bottlenecks and implemented caching (Action).
    We improved performance by 50% and met the deadline (Result).
    """
    
    evaluation = answer_evaluator.evaluate_answer(question, answer)
    assert evaluation['overall_score'] > 0
    assert 'feedback' in evaluation
