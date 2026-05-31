"""
ATS (Applicant Tracking System) Scoring Engine
Evaluates resumes using TF-IDF and cosine similarity
"""

from typing import Dict, List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.nlp_engine import nlp_engine
from app.services.skill_extractor import skill_extractor
from app.utils.text_cleaner import TextCleaner
from app.core.logging import get_logger

logger = get_logger(__name__)


class ATSScorer:
    """ATS scoring engine for resume evaluation"""
    
    # Sample job descriptions for comparison (can be extended)
    JOB_DESCRIPTIONS = {
        "software_engineer": """
            Software Engineer position requiring strong programming skills in Python, Java, or JavaScript.
            Experience with web development, APIs, databases, and version control (Git).
            Knowledge of data structures, algorithms, and software design patterns.
            Bachelor's degree in Computer Science or related field.
            Strong problem-solving and communication skills required.
        """,
        "data_scientist": """
            Data Scientist role requiring expertise in machine learning, statistical analysis,
            and data visualization. Proficiency in Python, pandas, numpy, scikit-learn, and SQL.
            Experience with deep learning frameworks like TensorFlow or PyTorch.
            Strong analytical skills and ability to communicate findings to stakeholders.
            Master's degree in Data Science, Statistics, or related field preferred.
        """,
        "frontend_developer": """
            Frontend Developer position requiring expertise in HTML, CSS, JavaScript, and modern
            frameworks like React, Angular, or Vue. Experience with responsive design,
            cross-browser compatibility, and web performance optimization.
            Knowledge of version control (Git) and agile methodologies.
            Portfolio demonstrating frontend projects required.
        """,
        "devops_engineer": """
            DevOps Engineer role requiring experience with containerization (Docker, Kubernetes),
            CI/CD pipelines, and cloud platforms (AWS, Azure, or GCP).
            Proficiency in scripting (Python, Bash) and infrastructure as code (Terraform, Ansible).
            Knowledge of monitoring, logging, and security best practices.
            Bachelor's degree in Computer Science or equivalent experience.
        """,
        "full_stack_developer": """
            Full Stack Developer position requiring proficiency in both frontend and backend development.
            Experience with JavaScript, React, Node.js, databases (SQL and NoSQL).
            Knowledge of RESTful APIs, microservices, and cloud deployment.
            Strong understanding of software development lifecycle and agile methodologies.
            Bachelor's degree in Computer Science or related field.
        """
    }
    
    def __init__(self):
        """Initialize ATS scorer"""
        self.text_cleaner = TextCleaner()
        self.vectorizer = None
    
    def calculate_ats_score(
        self,
        resume_text: str,
        parsed_data: Dict,
        job_description: str = None,
        target_role: str = None
    ) -> Dict[str, any]:
        """
        Calculate comprehensive ATS score
        
        Args:
            resume_text: Raw resume text
            parsed_data: Parsed resume data
            job_description: Optional job description for comparison
            target_role: Optional target role for scoring
            
        Returns:
            Dictionary with scores and feedback
        """
        logger.info("Calculating ATS score")
        
        # Select job description
        if not job_description:
            job_description = self._select_job_description(target_role, parsed_data)
        
        # Calculate component scores
        keyword_score = self._calculate_keyword_score(resume_text, job_description)
        tfidf_score = self._calculate_tfidf_similarity(resume_text, job_description)
        skill_score = self._calculate_skill_score(parsed_data, job_description)
        format_score = self._calculate_format_score(parsed_data)
        experience_score = self._calculate_experience_score(parsed_data)
        education_score = self._calculate_education_score(parsed_data)
        
        # Calculate weighted overall score
        overall_score = self._calculate_weighted_score({
            "keyword_match": keyword_score,
            "tfidf_similarity": tfidf_score,
            "skill_match": skill_score,
            "format_quality": format_score,
            "experience": experience_score,
            "education": education_score
        })
        
        # Identify missing keywords
        missing_keywords = self._identify_missing_keywords(resume_text, job_description)
        
        # Generate weak areas
        weak_areas = self._identify_weak_areas({
            "keyword_match": keyword_score,
            "skill_match": skill_score,
            "format_quality": format_score,
            "experience": experience_score,
            "education": education_score
        })
        
        # Generate improvement suggestions
        improvements = self._generate_improvements(
            parsed_data,
            missing_keywords,
            weak_areas
        )
        
        result = {
            "overall_score": overall_score,
            "component_scores": {
                "keyword_match": round(keyword_score, 2),
                "tfidf_similarity": round(tfidf_score, 2),
                "skill_match": round(skill_score, 2),
                "format_quality": round(format_score, 2),
                "experience_score": round(experience_score, 2),
                "education_score": round(education_score, 2)
            },
            "analysis": {
                "missing_keywords": missing_keywords[:15],
                "weak_areas": weak_areas,
                "strengths": self._identify_strengths(parsed_data),
                "recommendations": improvements
            },
            "score_interpretation": self._interpret_score(overall_score)
        }
        
        logger.info(f"ATS score calculated: {overall_score}/100")
        return result
    
    def _select_job_description(self, target_role: str, parsed_data: Dict) -> str:
        """Select appropriate job description"""
        if target_role:
            role_key = target_role.lower().replace(" ", "_")
            if role_key in self.JOB_DESCRIPTIONS:
                return self.JOB_DESCRIPTIONS[role_key]
        
        # Auto-detect based on skills
        skills = parsed_data.get("skills", {}).get("technical_skills", [])
        skill_str = " ".join(skills).lower()
        
        if any(word in skill_str for word in ["react", "angular", "vue", "css"]):
            return self.JOB_DESCRIPTIONS["frontend_developer"]
        elif any(word in skill_str for word in ["docker", "kubernetes", "devops", "jenkins"]):
            return self.JOB_DESCRIPTIONS["devops_engineer"]
        elif any(word in skill_str for word in ["machine learning", "tensorflow", "data science"]):
            return self.JOB_DESCRIPTIONS["data_scientist"]
        else:
            return self.JOB_DESCRIPTIONS["software_engineer"]
    
    def _calculate_keyword_score(self, resume_text: str, job_description: str) -> float:
        """
        Calculate keyword match score
        
        Args:
            resume_text: Resume text
            job_description: Job description
            
        Returns:
            Score (0-100)
        """
        # Extract keywords from job description
        jd_keywords = nlp_engine.extract_keywords(job_description, top_n=30)
        jd_words = {word for word, score in jd_keywords}
        
        # Extract keywords from resume
        resume_keywords = nlp_engine.extract_keywords(resume_text, top_n=50)
        resume_words = {word for word, score in resume_keywords}
        
        # Calculate match percentage
        matches = jd_words & resume_words
        if not jd_words:
            return 100.0
        
        score = (len(matches) / len(jd_words)) * 100
        return min(score, 100.0)
    
    def _calculate_tfidf_similarity(self, resume_text: str, job_description: str) -> float:  """
        Calculate TF-IDF cosine similarity
        
        Args:
            resume_text: Resume text
            job_description: Job description
            
        Returns:
            Similarity score (0-100)
        """
        similarity = nlp_engine.compute_tfidf_similarity(
            resume_text,
            job_description,
            use_bigrams=True
        )
        
        # Convert to percentage
        return similarity * 100
    
    def _calculate_skill_score(self, parsed_data: Dict, job_description: str) -> float:
        """
        Calculate skill match score
        
        Args:
            parsed_data: Parsed resume data
            job_description: Job description
            
        Returns:
            Score (0-100)
        """
        # Extract skills from resume
        resume_skills = set(
            skill.lower() 
            for skill in parsed_data.get("skills", {}).get("technical_skills", [])
        )
        
        # Extract required skills from job description
        jd_skills = skill_extractor.extract_skills(job_description)
        required_skills = set(
            skill.lower() 
            for skill in jd_skills.get("technical_skills", [])
        )
        
        if not required_skills:
            return 100.0
        
        # Calculate match
        matches = resume_skills & required_skills
        score = (len(matches) / len(required_skills)) * 100
        
        return min(score, 100.0)
    
    def _calculate_format_score(self, parsed_data: Dict) -> float:
        """
        Calculate resume format quality score
        
        Args:
            parsed_data: Parsed resume data
            
        Returns:
            Score (0-100)
        """
        score = 0.0
        max_score = 100.0
        
        # Check for contact information (20 points)
        contact = parsed_data.get("contact_info", {})
        if contact.get("emails"):
            score += 10
        if contact.get("phones"):
            score += 10
        
        # Check for key sections (40 points)
        if parsed_data.get("education"):
            score += 15
        if parsed_data.get("experience"):
            score += 15
        if parsed_data.get("skills", {}).get("all_skills"):
            score += 10
        
        # Check for optional but valuable sections (20 points)
        if parsed_data.get("projects"):
            score += 10
        if parsed_data.get("certifications"):
            score += 10
        
        # Check language quality (20 points)
        lang_quality = parsed_data.get("language_quality", {})
        avg_sentence_length = lang_quality.get("avg_sentence_length", 0)
        
        if 15 <= avg_sentence_length <= 25:  # Ideal sentence length
            score += 10
        elif 10 <= avg_sentence_length <= 30:
            score += 5
        
        if lang_quality.get("total_words", 0) > 200:  # Sufficient content
            score += 10
        elif lang_quality.get("total_words", 0) > 100:
            score += 5
        
        return min(score, max_score)
    
    def _calculate_experience_score(self, parsed_data: Dict) -> float:
        """
        Calculate experience score
        
        Args:
            parsed_data: Parsed resume data
            
        Returns:
            Score (0-100)
        """
        experience = parsed_data.get("experience", [])
        total_years = parsed_data.get("total_experience_years", 0)
        
        score = 0.0
        
        # Years of experience (up to 50 points)
        if total_years >= 5:
            score += 50
        elif total_years >= 3:
            score += 40
        elif total_years >= 1:
            score += 30
        elif total_years > 0:
            score += 20
        
        # Number of positions (up to 25 points)
        num_positions = len(experience)
        if num_positions >= 4:
            score += 25
        elif num_positions >= 3:
            score += 20
        elif num_positions >= 2:
            score += 15
        elif num_positions >= 1:
            score += 10
        
        # Quality of experience descriptions (up to 25 points)
        total_desc_length = sum(
            len(exp.get("description", "")) 
            for exp in experience
        )
        
        if total_desc_length > 500:
            score += 25
        elif total_desc_length > 250:
            score += 15
        elif total_desc_length > 100:
            score += 10
        
        return min(score, 100.0)
    
    def _calculate_education_score(self, parsed_data: Dict) -> float:
        """
        Calculate education score
        
        Args:
            parsed_data: Parsed resume data
            
        Returns:
            Score (0-100)
        """
        education = parsed_data.get("education", [])
        
        if not education:
            return 50.0  # Not everyone needs formal education
        
        score = 60.0  # Base score for having education
        
        for edu in education:
            degree = edu.get("degree", "").lower()
            
            # Doctoral degree
            if any(word in degree for word in ["phd", "doctorate", "doctor"]):
                score += 40
                break
            # Master's degree
            elif any(word in degree for word in ["master", "m.s", "m.tech", "mba"]):
                score += 30
                break
            # Bachelor's degree
            elif any(word in degree for word in ["bachelor", "b.s", "b.tech", "b.e"]):
                score += 20
                break
        
        return min(score, 100.0)
    
    def _calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """
        Calculate weighted overall score
        
        Args:
            scores: Dictionary of component scores
            
        Returns:
            Weighted overall score
        """
        weights = {
            "keyword_match": 0.25,
            "tfidf_similarity": 0.20,
            "skill_match": 0.25,
            "format_quality": 0.10,
            "experience": 0.12,
            "education": 0.08
        }
        
        weighted_score = sum(
            scores.get(key, 0) * weight
            for key, weight in weights.items()
        )
        
        return round(weighted_score, 2)
    
    def _identify_missing_keywords(
        self,
        resume_text: str,
        job_description: str
    ) -> List[str]:
        """
        Identify keywords missing from resume
        
        Args:
            resume_text: Resume text
            job_description: Job description
            
        Returns:
            List of missing keywords
        """
        # Extract keywords from job description
        jd_keywords = nlp_engine.extract_keywords(job_description, top_n=30)
        jd_words = {word for word, score in jd_keywords}
        
        # Extract keywords from resume
        resume_keywords = nlp_engine.extract_keywords(resume_text, top_n=50)
        resume_words = {word for word, score in resume_keywords}
        
        # Find missing keywords
        missing = jd_words - resume_words
        
        # Sort by importance (based on JD keyword frequency)
        jd_keyword_dict = dict(jd_keywords)
        missing_sorted = sorted(
            missing,
            key=lambda x: jd_keyword_dict.get(x, 0),
            reverse=True
        )
        
        return missing_sorted
    
    def _identify_weak_areas(self, scores: Dict[str, float]) -> List[str]:
        """
        Identify weak areas based on component scores
        
        Args:
            scores: Component scores
            
        Returns:
            List of weak areas
        """
        weak_areas = []
        
        threshold = 60.0  # Scores below this are considered weak
        
        area_names = {
            "keyword_match": "Keyword optimization",
            "skill_match": "Required skills coverage",
            "format_quality": "Resume formatting and structure",
            "experience": "Work experience details",
            "education": "Education section"
        }
        
        for key, score in scores.items():
            if score < threshold and key in area_names:
                weak_areas.append(area_names[key])
        
        return weak_areas
    
    def _identify_strengths(self, parsed_data: Dict) -> List[str]:
        """
        Identify resume strengths
        
        Args:
            parsed_data: Parsed resume data
            
        Returns:
            List of strengths
        """
        strengths = []
        
        # Check technical skills
        skills = parsed_data.get("skills", {}).get("technical_skills", [])
        if len(skills) >= 10:
            strengths.append(f"Strong technical skill set ({len(skills)} skills)")
        
        # Check experience
        total_years = parsed_data.get("total_experience_years", 0)
        if total_years >= 3:
            strengths.append(f"Solid work experience ({total_years} years)")
        
        # Check projects
        projects = parsed_data.get("projects", [])
        if len(projects) >= 3:
            strengths.append(f"Good project portfolio ({len(projects)} projects)")
        
        # Check certifications
        certs = parsed_data.get("certifications", [])
        if certs:
            strengths.append(f"Professional certifications ({len(certs)})")
        
        # Check contact info
        contact = parsed_data.get("contact_info", {})
        if contact.get("linkedin") or contact.get("github"):
            strengths.append("Professional online presence")
        
        return strengths if strengths else ["Resume has good foundational elements"]
    
    def _generate_improvements(
        self,
        parsed_data: Dict,
        missing_keywords: List[str],
        weak_areas: List[str]
    ) -> List[str]:
        """
        Generate improvement suggestions
        
        Args:
            parsed_data: Parsed resume data
            missing_keywords: Missing keywords
            weak_areas: Weak areas
            
        Returns:
            List of improvement suggestions
        """
        improvements = []
        
        # Keyword improvements
        if missing_keywords:
            improvements.append(
                f"Add these relevant keywords: {', '.join(missing_keywords[:8])}"
            )
        
        # Skill improvements
        skills = parsed_data.get("skills", {}).get("technical_skills", [])
        if len(skills) < 5:
            improvements.append(
                "Add more technical skills and technologies you've worked with"
            )
        
        # Experience improvements
        experience = parsed_data.get("experience", [])
        if len(experience) < 2:
            improvements.append(
                "Include more work experience entries with detailed descriptions"
            )
        
        # Project improvements
        projects = parsed_data.get("projects", [])
        if len(projects) < 2:
            improvements.append(
                "Add technical projects to demonstrate practical skills"
            )
        
        # Certification improvements
        certs = parsed_data.get("certifications", [])
        if not certs:
            improvements.append(
                "Consider adding relevant certifications to boost credibility"
            )
        
        # Contact improvements
        contact = parsed_data.get("contact_info", {})
        if not contact.get("linkedin"):
            improvements.append("Add LinkedIn profile for professional networking")
        if not contact.get("github") and len(skills) > 0:
            improvements.append("Include GitHub profile to showcase code samples")
        
        # Format improvements
        if "Resume formatting and structure" in weak_areas:
            improvements.append(
                "Improve resume structure with clear section headings"
            )
        
        return improvements[:10]  # Limit to top 10
    
    def _interpret_score(self, score: float) -> str:
        """
        Interpret ATS score with description
        
        Args:
            score: Overall score
            
        Returns:
            Score interpretation
        """
        if score >= 85:
            return "Excellent - Your resume is highly optimized for ATS"
        elif score >= 70:
            return "Good - Your resume should pass most ATS filters"
        elif score >= 55:
            return "Fair - Consider making improvements to increase chances"
        elif score >= 40:
            return "Needs Work - Significant improvements recommended"
        else:
            return "Poor - Major revisions needed for ATS compatibility"


# Global instance
ats_scorer = ATSScorer()
