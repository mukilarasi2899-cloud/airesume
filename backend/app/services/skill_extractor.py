"""
Skill Extraction and Clustering
Identifies technical and soft skills from resume text
"""

import json
from typing import List, Dict, Set
from pathlib import Path
import re

from app.services.nlp_engine import nlp_engine
from app.core.logging import get_logger

logger = get_logger(__name__)


class SkillExtractor:
    """Extract and categorize skills from resume text"""
    
    # Comprehensive skill database (can be extended)
    TECHNICAL_SKILLS = {
        # Programming Languages
        "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php",
        "go", "rust", "swift", "kotlin", "scala", "r", "matlab", "perl",
        
        # Web Technologies
        "html", "css", "react", "angular", "vue", "nodejs", "node.js", "express",
        "django", "flask", "fastapi", "spring", "asp.net", "laravel",
        "jquery", "bootstrap", "tailwind", "sass", "webpack", "vite",
        
        # Databases
        "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra",
        "oracle", "sqlite", "dynamodb", "elasticsearch", "mariadb",
        
        # Cloud & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "gitlab",
        "github actions", "terraform", "ansible", "chef", "puppet",
        "circleci", "travis ci", "heroku", "netlify", "vercel",
        
        # Data Science & ML
        "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
        "scikit-learn", "pandas", "numpy", "scipy", "matplotlib", "seaborn",
        "nlp", "computer vision", "data analysis", "data visualization",
        "tableau", "power bi", "apache spark", "hadoop",
        
        # Mobile Development
        "android", "ios", "react native", "flutter", "xamarin", "ionic",
        
        # Other Technologies
        "git", "linux", "bash", "powershell", "api", "rest", "graphql",
        "microservices", "agile", "scrum", "jira", "confluence",
    }
    
    SOFT_SKILLS = {
        "leadership", "communication", "teamwork", "problem solving",
        "critical thinking", "time management", "adaptability", "creativity",
        "attention to detail", "collaboration", "project management",
        "analytical", "presentation", "negotiation", "mentoring",
    }
    
    # Skill categories for clustering
    SKILL_CATEGORIES = {
        "Programming": [
            "python", "java", "javascript", "typescript", "c++", "c#",
            "ruby", "php", "go", "rust", "swift", "kotlin"
        ],
        "Web Development": [
            "html", "css", "react", "angular", "vue", "nodejs", "django",
            "flask", "fastapi", "express", "jquery", "bootstrap"
        ],
        "Database": [
            "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra",
            "oracle", "sqlite", "dynamodb", "elasticsearch"
        ],
        "Cloud & DevOps": [
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
            "terraform", "ansible", "gitlab", "github actions"
        ],
        "Data Science": [
            "machine learning", "deep learning", "tensorflow", "pytorch",
            "pandas", "numpy", "data analysis", "nlp", "computer vision"
        ],
        "Mobile": [
            "android", "ios", "react native", "flutter", "xamarin"
        ],
        "Tools & Methodologies": [
            "git", "agile", "scrum", "jira", "api", "rest", "graphql",
            "microservices", "linux", "bash"
        ],
    }
    
    def __init__(self):
        """Initialize skill extractor"""
        self.all_skills = self.TECHNICAL_SKILLS | self.SOFT_SKILLS
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills from resume text
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with categorized skills
        """
        text_lower = text.lower()
        
        # Strategy 1: Direct matching with known skills
        found_technical = set()
        found_soft = set()
        
        for skill in self.TECHNICAL_SKILLS:
            # Use word boundaries for accurate matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_technical.add(skill)
        
        for skill in self.SOFT_SKILLS:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_soft.add(skill)
        
        # Strategy 2: Use NLP to find additional skills
        skill_candidates = nlp_engine.extract_skill_candidates(text)
        
        for candidate in skill_candidates:
            candidate_lower = candidate.lower()
            # Check if candidate is similar to known skills
            for skill in self.all_skills:
                if skill in candidate_lower or candidate_lower in skill:
                    if skill in self.TECHNICAL_SKILLS:
                        found_technical.add(skill)
                    else:
                        found_soft.add(skill)
        
        return {
            "technical_skills": sorted(list(found_technical)),
            "soft_skills": sorted(list(found_soft)),
            "all_skills": sorted(list(found_technical | found_soft))
        }
    
    def cluster_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """
        Cluster skills into categories
        
        Args:
            skills: List of skills
            
        Returns:
            Dictionary of categories and their skills
        """
        clustered = {category: [] for category in self.SKILL_CATEGORIES}
        uncategorized = []
        
        for skill in skills:
            skill_lower = skill.lower()
            categorized = False
            
            for category, category_skills in self.SKILL_CATEGORIES.items():
                if skill_lower in category_skills:
                    clustered[category].append(skill)
                    categorized = True
                    break
            
            if not categorized:
                uncategorized.append(skill)
        
        if uncategorized:
            clustered["Other"] = uncategorized
        
        # Remove empty categories
        clustered = {k: v for k, v in clustered.items() if v}
        
        return clustered
    
    def analyze_skill_proficiency(
        self,
        text: str,
        skills: List[str]
    ) -> Dict[str, Dict[str, any]]:
        """
        Analyze skill proficiency based on context
        
        Args:
            text: Resume text
            skills: List of identified skills
            
        Returns:
            Dictionary with skill proficiency analysis
        """
        text_lower = text.lower()
        proficiency_keywords = {
            "expert": ["expert", "advanced", "proficient", "mastery"],
            "intermediate": ["intermediate", "working knowledge", "familiar"],
            "beginner": ["beginner", "basic", "fundamental", "learning"]
        }
        
        analysis = {}
        
        for skill in skills:
            # Find context around skill mention
            pattern = r'.{0,50}\b' + re.escape(skill.lower()) + r'\b.{0,50}'
            matches = re.findall(pattern, text_lower)
            
            proficiency = "unspecified"
            mentions = len(matches)
            
            # Analyze context for proficiency indicators
            for match in matches:
                for level, keywords in proficiency_keywords.items():
                    if any(keyword in match for keyword in keywords):
                        proficiency = level
                        break
            
            analysis[skill] = {
                "proficiency": proficiency,
                "mentions": mentions,
                "contexts": matches[:3]  # Store up to 3 contexts
            }
        
        return analysis
    
    def suggest_missing_skills(
        self,
        found_skills: List[str],
        target_role: str
    ) -> List[str]:
        """
        Suggest missing skills for a target role
        
        Args:
            found_skills: Skills found in resume
            target_role: Target job role
            
        Returns:
            List of suggested skills
        """
        role_lower = target_role.lower()
        found_lower = {skill.lower() for skill in found_skills}
        
        # Role-based skill requirements
        role_skills = {
            "software engineer": [
                "python", "java", "javascript", "git", "sql", "api",
                "data structures", "algorithms", "testing"
            ],
            "data scientist": [
                "python", "machine learning", "pandas", "numpy", "sql",
                "statistics", "data visualization", "tensorflow"
            ],
            "web developer": [
                "html", "css", "javascript", "react", "nodejs", "git",
                "rest", "responsive design"
            ],
            "devops engineer": [
                "docker", "kubernetes", "aws", "jenkins", "linux",
                "bash", "terraform", "monitoring"
            ],
            "mobile developer": [
                "android", "ios", "react native", "api", "git",
                "mobile ui", "testing"
            ],
        }
        
        # Find best matching role
        matching_role = None
        for role_key in role_skills:
            if role_key in role_lower:
                matching_role = role_key
                break
        
        if not matching_role:
            return []
        
        # Suggest missing skills
        required_skills = role_skills[matching_role]
        missing = [
            skill for skill in required_skills
            if skill.lower() not in found_lower
        ]
        
        return missing
    
    def calculate_skill_score(
        self,
        found_skills: List[str],
        required_skills: List[str]
    ) -> float:
        """
        Calculate skill match score
        
        Args:
            found_skills: Skills found in resume
            required_skills: Required skills for job
            
        Returns:
            Match score (0-100)
        """
        if not required_skills:
            return 100.0
        
        found_lower = {skill.lower() for skill in found_skills}
        required_lower = {skill.lower() for skill in required_skills}
        
        matches = found_lower & required_lower
        score = (len(matches) / len(required_lower)) * 100
        
        return round(score, 2)
    
    def recommend_job_roles(self, skills: List[str], top_n: int = 5) -> List[Dict[str, any]]:
        """
        Recommend job roles based on skills
        
        Args:
            skills: List of skills
            top_n: Number of recommendations
            
        Returns:
            List of recommended roles with match scores
        """
        skills_lower = {skill.lower() for skill in skills}
        
        # Role definitions with required skills
        role_definitions = {
            "Software Engineer": [
                "python", "java", "javascript", "git", "sql", "api"
            ],
            "Full Stack Developer": [
                "javascript", "react", "nodejs", "html", "css", "sql", "git"
            ],
            "Data Scientist": [
                "python", "machine learning", "pandas", "sql", "statistics"
            ],
            "ML Engineer": [
                "python", "tensorflow", "pytorch", "machine learning", "docker"
            ],
            "DevOps Engineer": [
                "docker", "kubernetes", "aws", "jenkins", "linux", "terraform"
            ],
            "Frontend Developer": [
                "javascript", "react", "html", "css", "typescript"
            ],
            "Backend Developer": [
                "python", "java", "sql", "api", "microservices"
            ],
            "Mobile Developer": [
                "android", "ios", "react native", "mobile development"
            ],
            "Data Analyst": [
                "sql", "python", "excel", "tableau", "data analysis"
            ],
            "QA Engineer": [
                "testing", "selenium", "automation", "api testing"
            ],
        }
        
        recommendations = []
        
        for role, required in role_definitions.items():
            required_lower = {s.lower() for s in required}
            matches = skills_lower & required_lower
            match_score = (len(matches) / len(required_lower)) * 100
            
            if match_score > 0:
                recommendations.append({
                    "role": role,
                    "match_score": round(match_score, 2),
                    "matched_skills": list(matches),
                    "missing_skills": list(required_lower - skills_lower)
                })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        return recommendations[:top_n]


# Global instance
skill_extractor = SkillExtractor()
