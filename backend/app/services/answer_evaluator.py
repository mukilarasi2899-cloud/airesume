"""
Answer Evaluation System
Evaluates interview answers using NLP similarity scoring and keyword matching
"""

from typing import Dict, List, Tuple
import numpy as np

from app.services.nlp_engine import nlp_engine
from app.utils.text_cleaner import TextCleaner
from app.core.logging import get_logger

logger = get_logger(__name__)


class AnswerEvaluator:
    """Evaluate interview answers and provide feedback"""
    
    # Sample reference answers for common questions (can be extended)
    REFERENCE_ANSWERS = {
        "stack_queue": """
            A stack is a Last-In-First-Out (LIFO) data structure where elements are added 
            and removed from the same end. Use stacks for function call management, undo operations, 
            and depth-first search. A queue is First-In-First-Out (FIFO) where elements are added 
            at the rear and removed from the front. Use queues for breadth-first search, task scheduling, 
            and handling requests in order.
        """,
        "oop_concepts": """
            Object-Oriented Programming has four main pillars: Encapsulation bundles data and methods 
            together hiding internal details. Inheritance allows classes to inherit properties from parent 
            classes promoting code reuse. Polymorphism enables objects to take multiple forms through 
            method overriding and overloading. Abstraction hides complex implementation details showing 
            only essential features.
        """,
        "supervised_unsupervised": """
            Supervised learning uses labeled data where input-output pairs are known. Examples include 
            classification and regression tasks. The model learns from training data with correct answers. 
            Unsupervised learning works with unlabeled data finding hidden patterns. Examples include 
            clustering and dimensionality reduction. It discovers structure without predefined labels.
        """,
    }
    
    def __init__(self):
        """Initialize answer evaluator"""
        self.text_cleaner = TextCleaner()
    
    def evaluate_answer(
        self,
        user_answer: str,
        question: Dict,
        reference_answer: str = None
    ) -> Dict:
        """
        Comprehensive answer evaluation
        
        Args:
            user_answer: User's answer text
            question: Question dictionary with expected keywords
            reference_answer: Optional reference answer
            
        Returns:
            Evaluation results with scores and feedback
        """
        logger.info(f"Evaluating answer for question: {question.get('question_id')}")
        
        # Clean and validate answer
        cleaned_answer = self.text_cleaner.clean_text(user_answer)
        
        if not cleaned_answer or len(cleaned_answer) < 10:
            return self._generate_insufficient_answer_feedback()
        
        # Calculate component scores
        keyword_score = self._calculate_keyword_coverage(
            cleaned_answer,
            question.get("expected_keywords", [])
        )
        
        # Similarity scoring
        if reference_answer:
            semantic_score = self._calculate_semantic_similarity(
                cleaned_answer,
                reference_answer
            )
        else:
            semantic_score = self._estimate_quality_score(cleaned_answer)
        
        # Content analysis
        concept_score = self._analyze_concept_coverage(
            cleaned_answer,
            question
        )
        
        # Communication quality
        communication_score = self._evaluate_communication(cleaned_answer)
        
        # Calculate overall score
        overall_score = self._calculate_weighted_answer_score({
            "keyword_coverage": keyword_score,
            "semantic_similarity": semantic_score,
            "concept_coverage": concept_score,
            "communication": communication_score
        })
        
        # Identify missing key points
        missing_keywords = self._identify_missing_keywords(
            cleaned_answer,
            question.get("expected_keywords", [])
        )
        
        # Generate detailed feedback
        feedback = self._generate_feedback(
            user_answer=cleaned_answer,
            question=question,
            scores={
                "keyword_coverage": keyword_score,
                "semantic_similarity": semantic_score,
                "concept_coverage": concept_score,
                "communication": communication_score
            },
            missing_keywords=missing_keywords
        )
        
        result = {
            "overall_score": round(overall_score, 2),
            "score_percentage": round(overall_score, 2),
            "component_scores": {
                "keyword_coverage": round(keyword_score, 2),
                "semantic_similarity": round(semantic_score, 2),
                "concept_coverage": round(concept_score, 2),
                "communication_quality": round(communication_score, 2)
            },
            "analysis": {
                "answer_length": len(cleaned_answer),
                "word_count": len(cleaned_answer.split()),
                "keywords_matched": len(question.get("expected_keywords", [])) - len(missing_keywords),
                "keywords_total": len(question.get("expected_keywords", [])),
                "missing_keywords": missing_keywords
            },
            "feedback": feedback,
            "grade": self._assign_grade(overall_score)
        }
        
        logger.info(f"Answer evaluated: Score={overall_score}/100")
        return result
    
    def _calculate_keyword_coverage(
        self,
        answer: str,
        expected_keywords: List[str]
    ) -> float:
        """
        Calculate what percentage of expected keywords are present
        
        Args:
            answer: User's answer
            expected_keywords: List of expected keywords
            
        Returns:
            Coverage score (0-100)
        """
        if not expected_keywords:
            return 100.0
        
        answer_lower = answer.lower()
        
        # Count matched keywords (allowing partial matches)
        matched = 0
        for keyword in expected_keywords:
            keyword_lower = keyword.lower()
            # Check for exact word match or as part of compound word
            if keyword_lower in answer_lower:
                matched += 1
        
        score = (matched / len(expected_keywords)) * 100
        return min(score, 100.0)
    
    def _calculate_semantic_similarity(
        self,
        user_answer: str,
        reference_answer: str
    ) -> float:
        """
        Calculate semantic similarity between user and reference answer
        
        Args:
            user_answer: User's answer
            reference_answer: Reference answer
            
        Returns:
            Similarity score (0-100)
        """
        # Use both spaCy similarity and TF-IDF
        spacy_sim = nlp_engine.compute_similarity(user_answer, reference_answer)
        tfidf_sim = nlp_engine.compute_tfidf_similarity(
            user_answer,
            reference_answer,
            use_bigrams=True
        )
        
        # Weighted average
        combined_score = (spacy_sim * 0.4 + tfidf_sim * 0.6) * 100
        
        return min(combined_score, 100.0)
    
    def _estimate_quality_score(self, answer: str) -> float:
        """
        Estimate answer quality without reference answer
        
        Args:
            answer: User's answer
            
        Returns:
            Quality score (0-100)
        """
        score = 50.0  # Base score
        
        # Length-based scoring
        word_count = len(answer.split())
        
        if word_count >= 50:
            score += 20
        elif word_count >= 30:
            score += 15
        elif word_count >= 20:
            score += 10
        elif word_count >= 10:
            score += 5
        
        # Check for technical terms or depth
        doc = nlp_engine.nlp(answer)
        
        # Count entities and noun phrases (indicators of detailed answer)
        entities = len(doc.ents)
        noun_phrases = len(list(doc.noun_chunks))
        
        if entities > 3:
            score += 10
        elif entities > 1:
            score += 5
        
        if noun_phrases > 5:
            score += 10
        elif noun_phrases > 3:
            score += 5
        
        # Check for examples (phrases like "for example", "such as")
        example_phrases = ["for example", "such as", "for instance", "like"]
        if any(phrase in answer.lower() for phrase in example_phrases):
            score += 5
        
        return min(score, 100.0)
    
    def _analyze_concept_coverage(self, answer: str, question: Dict) -> float:
        """
        Analyze how well key concepts are covered
        
        Args:
            answer: User's answer
            question: Question details
            
        Returns:
            Concept coverage score (0-100)
        """
        category = question.get("category", "").lower()
        answer_lower = answer.lower()
        
        # Category-specific concept keywords
        concept_keywords = {
            "data structures": ["structure", "time complexity", "space", "operation"],
            "machine learning": ["model", "training", "data", "algorithm", "prediction"],
            "web development": ["http", "request", "response", "client", "server"],
            "database": ["query", "table", "data", "schema", "relationship"],
            "programming": ["code", "function", "variable", "logic", "syntax"],
        }
        
        # Find relevant concept keywords
        relevant_keywords = []
        for cat, keywords in concept_keywords.items():
            if cat in category:
                relevant_keywords = keywords
                break
        
        if not relevant_keywords:
            return 70.0  # Default score if no specific concepts defined
        
        # Count matching concepts
        matched_concepts = sum(
            1 for keyword in relevant_keywords
            if keyword in answer_lower
        )
        
        score = (matched_concepts / len(relevant_keywords)) * 100
        
        # Boost score if answer is detailed
        if len(answer.split()) > 40:
            score += 10
        
        return min(score, 100.0)
    
    def _evaluate_communication(self, answer: str) -> float:
        """
        Evaluate communication quality
        
        Args:
            answer: User's answer
            
        Returns:
            Communication score (0-100)
        """
        score = 60.0  # Base score
        
        # Analyze language quality
        lang_quality = nlp_engine.detect_language_quality(answer)
        
        # Sentence structure
        avg_sentence_length = lang_quality.get("avg_sentence_length", 0)
        
        if 10 <= avg_sentence_length <= 25:  # Ideal range
            score += 15
        elif 8 <= avg_sentence_length <= 30:
            score += 10
        elif avg_sentence_length > 0:
            score += 5
        
        # Vocabulary richness (unique words ratio)
        total_words = lang_quality.get("total_words", 1)
        unique_words = lang_quality.get("unique_words", 0)
        richness = unique_words / total_words if total_words > 0 else 0
        
        if richness > 0.7:
            score += 15
        elif richness > 0.5:
            score += 10
        elif richness > 0.3:
            score += 5
        
        # Check for structure (paragraphs, organization)
        sentences = nlp_engine.extract_sentences(answer)
        if len(sentences) >= 3:
            score += 10
        elif len(sentences) >= 2:
            score += 5
        
        return min(score, 100.0)
    
    def _calculate_weighted_answer_score(self, scores: Dict[str, float]) -> float:
        """
        Calculate weighted overall score
        
        Args:
            scores: Component scores
            
        Returns:
            Weighted score (0-100)
        """
        weights = {
            "keyword_coverage": 0.30,
            "semantic_similarity": 0.30,
            "concept_coverage": 0.25,
            "communication": 0.15
        }
        
        weighted_score = sum(
            scores.get(key, 0) * weight
            for key, weight in weights.items()
        )
        
        return min(weighted_score, 100.0)
    
    def _identify_missing_keywords(
        self,
        answer: str,
        expected_keywords: List[str]
    ) -> List[str]:
        """
        Identify keywords missing from answer
        
        Args:
            answer: User's answer
            expected_keywords: Expected keywords
            
        Returns:
            List of missing keywords
        """
        answer_lower = answer.lower()
        
        missing = [
            keyword for keyword in expected_keywords
            if keyword.lower() not in answer_lower
        ]
        
        return missing
    
    def _generate_feedback(
        self,
        user_answer: str,
        question: Dict,
        scores: Dict[str, float],
        missing_keywords: List[str]
    ) -> Dict[str, any]:
        """
        Generate detailed feedback
        
        Args:
            user_answer: User's answer
            question: Question details
            scores: Component scores
            missing_keywords: Missing keywords
            
        Returns:
            Feedback dictionary
        """
        feedback = {
            "summary": "",
            "strengths": [],
            "improvements": [],
            "missing_points": [],
            "suggestions": []
        }
        
        overall = sum(scores.values()) / len(scores)
        
        # Summary
        if overall >= 80:
            feedback["summary"] = "Excellent answer! You demonstrated strong understanding."
        elif overall >= 65:
            feedback["summary"] = "Good answer with room for minor improvements."
        elif overall >= 50:
            feedback["summary"] = "Decent answer, but missing some key points."
        else:
            feedback["summary"] = "Answer needs significant improvement."
        
        # Identify strengths
        if scores["keyword_coverage"] >= 70:
            feedback["strengths"].append("Good coverage of key concepts")
        
        if scores["communication"] >= 70:
            feedback["strengths"].append("Clear and well-structured response")
        
        if len(user_answer.split()) >= 40:
            feedback["strengths"].append("Detailed and comprehensive explanation")
        
        # Identify improvements
        if scores["keyword_coverage"] < 60:
            feedback["improvements"].append(
                "Include more relevant technical terms and concepts"
            )
        
        if scores["concept_coverage"] < 60:
            feedback["improvements"].append(
                f"Provide deeper explanation of {question.get('category', 'concepts')}"
            )
        
        if scores["communication"] < 60:
            feedback["improvements"].append(
                "Improve answer structure and clarity"
            )
        
        if len(user_answer.split()) < 20:
            feedback["improvements"].append(
                "Provide more detailed explanation with examples"
            )
        
        # Missing points
        if missing_keywords:
            feedback["missing_points"] = [
                f"Consider mentioning: {', '.join(missing_keywords[:5])}"
            ]
        
        # Suggestions
        question_type = question.get("question_type", "")
        
        if question_type == "technical":
            feedback["suggestions"].extend([
                "Include practical examples or use cases",
                "Explain the 'why' behind concepts, not just 'what'",
                "Mention trade-offs or limitations where applicable"
            ])
        else:  # HR questions
            feedback["suggestions"].extend([
                "Use the STAR method (Situation, Task, Action, Result)",
                "Provide specific examples from your experience",
                "Quantify achievements where possible"
            ])
        
        return feedback
    
    def _assign_grade(self, score: float) -> str:
        """
        Assign letter grade based on score
        
        Args:
            score: Numerical score
            
        Returns:
            Letter grade
        """
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        elif score >= 50:
            return "C-"
        else:
            return "D"
    
    def _generate_insufficient_answer_feedback(self) -> Dict:
        """Generate feedback for insufficient answers"""
        return {
            "overall_score": 0.0,
            "score_percentage": 0.0,
            "component_scores": {
                "keyword_coverage": 0.0,
                "semantic_similarity": 0.0,
                "concept_coverage": 0.0,
                "communication_quality": 0.0
            },
            "analysis": {
                "answer_length": 0,
                "word_count": 0,
                "keywords_matched": 0,
                "keywords_total": 0,
                "missing_keywords": []
            },
            "feedback": {
                "summary": "Insufficient answer provided.",
                "strengths": [],
                "improvements": [
                    "Provide a substantive answer to the question",
                    "Include relevant technical details and concepts",
                    "Aim for at least 3-5 sentences"
                ],
                "missing_points": ["All key points are missing"],
                "suggestions": [
                    "Take time to think through the answer",
                    "Include examples to demonstrate understanding"
                ]
            },
            "grade": "F"
        }
    
    def evaluate_interview_performance(
        self,
        answers: List[Dict]
    ) -> Dict:
        """
        Evaluate overall interview performance
        
        Args:
            answers: List of answered questions with evaluations
            
        Returns:
            Overall performance analysis
        """
        if not answers:
            return {
                "overall_score": 0.0,
                "technical_score": 0.0,
                "hr_score": 0.0,
                "total_questions": 0,
                "performance_level": "Not Available"
            }
        
        technical_scores = [
            ans["evaluation"]["overall_score"]
            for ans in answers
            if ans.get("question_type") == "technical"
        ]
        
        hr_scores = [
            ans["evaluation"]["overall_score"]
            for ans in answers
            if ans.get("question_type") == "hr"
        ]
        
        all_scores = [ans["evaluation"]["overall_score"] for ans in answers]
        
        overall_avg = np.mean(all_scores) if all_scores else 0.0
        technical_avg = np.mean(technical_scores) if technical_scores else 0.0
        hr_avg = np.mean(hr_scores) if hr_scores else 0.0
        
        # Determine performance level
        if overall_avg >= 80:
            performance_level = "Excellent"
        elif overall_avg >= 70:
            performance_level = "Good"
        elif overall_avg >= 60:
            performance_level = "Average"
        elif overall_avg >= 50:
            performance_level = "Below Average"
        else:
            performance_level = "Needs Improvement"
        
        return {
            "overall_score": round(overall_avg, 2),
            "technical_score": round(technical_avg, 2),
            "hr_score": round(hr_avg, 2),
            "total_questions": len(answers),
            "technical_questions": len(technical_scores),
            "hr_questions": len(hr_scores),
            "performance_level": performance_level,
            "score_distribution": {
                "excellent": len([s for s in all_scores if s >= 80]),
                "good": len([s for s in all_scores if 70 <= s < 80]),
                "average": len([s for s in all_scores if 60 <= s < 70]),
                "below_average": len([s for s in all_scores if s < 60])
            }
        }


# Global instance
answer_evaluator = AnswerEvaluator()
