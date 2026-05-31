"""
Interview Question Generator
Dynamically generates technical and HR questions based on job role
"""

import random
from typing import List, Dict
from datetime import datetime

from app.core.logging import get_logger
from app.core.exceptions import InterviewGenerationError

logger = get_logger(__name__)


class QuestionGenerator:
    """Generate interview questions for various job roles"""
    
    # Comprehensive question bank organized by role and category
    QUESTION_BANK = {
        "software_engineer": {
            "technical": [ 
                {
                    "question": "Explain the difference between stack and queue data structures. When would you use each?",
                    "difficulty": "medium",
                    "keywords": ["stack", "queue", "lifo", "fifo", "data structure", "operations"],
                    "category": "Data Structures"
                },
                {
                    "question": "What is the time complexity of common operations in a hash table? How does it handle collisions?",
                    "difficulty": "medium",
                    "keywords": ["hash table", "time complexity", "collision", "hash function", "o(1)"],
                    "category": "Data Structures"
                },
                {
                    "question": "Explain object-oriented programming concepts: encapsulation, inheritance, polymorphism, and abstraction.",
                    "difficulty": "easy",
                    "keywords": ["oop", "encapsulation", "inheritance", "polymorphism", "abstraction", "classes"],
                    "category": "Programming Fundamentals"
                },
                {
                    "question": "What is the difference between SQL and NoSQL databases? Give examples of when to use each.",
                    "difficulty": "medium",
                    "keywords": ["sql", "nosql", "relational", "document", "database", "scalability"],
                    "category": "Databases"
                },
                {
                    "question": "Explain RESTful API principles. What are HTTP methods and status codes?",
                    "difficulty": "easy",
                    "keywords": ["rest", "api", "http", "get", "post", "put", "delete", "status codes"],
                    "category": "Web Development"
                },
                {
                    "question": "What is version control? Explain Git branching strategies.",
                    "difficulty": "easy",
                    "keywords": ["git", "version control", "branching", "merge", "commit", "pull request"],
                    "category": "Development Tools"
                },
                {
                    "question": "Describe the software development lifecycle (SDLC). What is Agile methodology?",
                    "difficulty": "easy",
                    "keywords": ["sdlc", "agile", "scrum", "sprint", "waterfall", "development process"],
                    "category": "Methodology"
                },
                {
                    "question": "What are design patterns? Explain Singleton, Factory, and Observer patterns.",
                    "difficulty": "hard",
                    "keywords": ["design patterns", "singleton", "factory", "observer", "architecture"],
                    "category": "Software Design"
                },
            ],
            "hr": [
                {
                    "question": "Tell me about a challenging bug you fixed. How did you approach debugging?",
                    "difficulty": "medium",
                    "keywords": ["debugging", "problem solving", "analytical", "systematic"],
                    "category": "Problem Solving"
                },
                {
                    "question": "Describe a time when you had to learn a new technology quickly for a project.",
                    "difficulty": "easy",
                    "keywords": ["learning", "adaptability", "self-motivated", "quick learner"],
                    "category": "Learning Ability"
                },
                {
                    "question": "How do you handle conflicting priorities or tight deadlines?",
                    "difficulty": "easy",
                    "keywords": ["time management", "prioritization", "pressure", "organization"],
                    "category": "Time Management"
                },
                {
                    "question": "Tell me about a project where you collaborated with a team. What was your role?",
                    "difficulty": "easy",
                    "keywords": ["teamwork", "collaboration", "communication", "contribution"],
                    "category": "Teamwork"
                },
            ]
        },
        "data_scientist": {
            "technical": [
                {
                    "question": "Explain the difference between supervised and unsupervised learning with examples.",
                    "difficulty": "easy",
                    "keywords": ["supervised", "unsupervised", "classification", "clustering", "machine learning"],
                    "category": "Machine Learning"
                },
                {
                    "question": "What is overfitting and underfitting? How do you prevent them?",
                    "difficulty": "medium",
                    "keywords": ["overfitting", "underfitting", "regularization", "cross-validation", "bias-variance"],
                    "category": "Machine Learning"
                },
                {
                    "question": "Explain the working of a Random Forest algorithm. What are its advantages?",
                    "difficulty": "medium",
                    "keywords": ["random forest", "ensemble", "decision tree", "bagging", "feature importance"],
                    "category": "Algorithms"
                },
                {
                    "question": "What is feature engineering? Give examples of techniques you've used.",
                    "difficulty": "medium",
                    "keywords": ["feature engineering", "feature selection", "dimensionality", "transformation"],
                    "category": "Data Preprocessing"
                },
                {
                    "question": "Explain the difference between precision, recall, and F1-score.",
                    "difficulty": "easy",
                    "keywords": ["precision", "recall", "f1-score", "evaluation", "metrics", "confusion matrix"],
                    "category": "Model Evaluation"
                },
                {
                    "question": "What is gradient descent? How does it work in neural networks?",
                    "difficulty": "hard",
                    "keywords": ["gradient descent", "optimization", "backpropagation", "learning rate", "convergence"],
                    "category": "Deep Learning"
                },
                {
                    "question": "How do you handle missing data in a dataset?",
                    "difficulty": "easy",
                    "keywords": ["missing data", "imputation", "data cleaning", "preprocessing"],
                    "category": "Data Preprocessing"
                },
            ],
            "hr": [
                {
                    "question": "Describe a data science project where you delivered actionable insights to stakeholders.",
                    "difficulty": "medium",
                    "keywords": ["communication", "business impact", "stakeholders", "insights"],
                    "category": "Communication"
                },
                {
                    "question": "How do you explain complex technical concepts to non-technical audiences?",
                    "difficulty": "medium",
                    "keywords": ["communication", "simplification", "visualization", "storytelling"],
                    "category": "Communication"
                },
                {
                    "question": "Tell me about a time when your model didn't perform as expected. What did you do?",
                    "difficulty": "medium",
                    "keywords": ["problem solving", "debugging", "iteration", "persistence"],
                    "category": "Problem Solving"
                },
            ]
        },
        "frontend_developer": {
            "technical": [
                {
                    "question": "Explain the difference between var, let, and const in JavaScript.",
                    "difficulty": "easy",
                    "keywords": ["javascript", "var", "let", "const", "scope", "hoisting"],
                    "category": "JavaScript"
                },
                {
                    "question": "What is the Virtual DOM in React? How does it improve performance?",
                    "difficulty": "medium",
                    "keywords": ["react", "virtual dom", "reconciliation", "performance", "rendering"],
                    "category": "React"
                },
                {
                    "question": "Explain CSS Flexbox and Grid. When would you use each?",
                    "difficulty": "easy",
                    "keywords": ["css", "flexbox", "grid", "layout", "responsive"],
                    "category": "CSS"
                },
                {
                    "question": "What are React Hooks? Explain useState and useEffect.",
                    "difficulty": "medium",
                    "keywords": ["react hooks", "usestate", "useeffect", "functional components", "lifecycle"],
                    "category": "React"
                },
                {
                    "question": "How do you optimize website performance and load time?",
                    "difficulty": "medium",
                    "keywords": ["performance", "optimization", "lazy loading", "caching", "minification"],
                    "category": "Performance"
                },
                {
                    "question": "Explain the concept of responsive design. What are media queries?",
                    "difficulty": "easy",
                    "keywords": ["responsive", "media queries", "mobile-first", "breakpoints"],
                    "category": "Responsive Design"
                },
            ],
            "hr": [
                {
                    "question": "Describe a UI/UX challenge you faced and how you solved it.",
                    "difficulty": "medium",
                    "keywords": ["ux", "user experience", "design", "problem solving"],
                    "category": "Design Thinking"
                },
                {
                    "question": "How do you stay updated with rapidly changing frontend technologies?",
                    "difficulty": "easy",
                    "keywords": ["learning", "continuous improvement", "trends", "community"],
                    "category": "Learning"
                },
            ]
        },
        "devops_engineer": {
            "technical": [
                {
                    "question": "Explain the difference between Docker containers and virtual machines.",
                    "difficulty": "easy",
                    "keywords": ["docker", "containers", "vm", "virtualization", "isolation"],
                    "category": "Containerization"
                },
                {
                    "question": "What is Kubernetes? Explain its core components.",
                    "difficulty": "medium",
                    "keywords": ["kubernetes", "pods", "nodes", "services", "orchestration"],
                    "category": "Container Orchestration"
                },
                {
                    "question": "Describe a CI/CD pipeline. What tools have you used?",
                    "difficulty": "easy",
                    "keywords": ["ci/cd", "jenkins", "gitlab", "automation", "deployment"],
                    "category": "CI/CD"
                },
                {
                    "question": "What is Infrastructure as Code? Explain Terraform or Ansible.",
                    "difficulty": "medium",
                    "keywords": ["iac", "terraform", "ansible", "automation", "infrastructure"],
                    "category": "IaC"
                },
                {
                    "question": "How do you monitor and troubleshoot production systems?",
                    "difficulty": "medium",
                    "keywords": ["monitoring", "logging", "troubleshooting", "observability", "alerts"],
                    "category": "Monitoring"
                },
            ],
            "hr": [
                {
                    "question": "Describe a production incident you handled. How did you resolve it?",
                    "difficulty": "medium",
                    "keywords": ["incident", "troubleshooting", "problem solving", "pressure"],
                    "category": "Incident Management"
                },
                {
                    "question": "How do you balance automation with manual intervention in your work?",
                    "difficulty": "medium",
                    "keywords": ["automation", "efficiency", "judgment", "balance"],
                    "category": "Methodology"
                },
            ]
        },
        "full_stack_developer": {
            "technical": [
                {
                    "question": "Explain the Model-View-Controller (MVC) architecture pattern.",
                    "difficulty": "easy",
                    "keywords": ["mvc", "architecture", "separation", "model", "view", "controller"],
                    "category": "Architecture"
                },
                {
                    "question": "What is the difference between authentication and authorization?",
                    "difficulty": "easy",
                    "keywords": ["authentication", "authorization", "security", "identity", "permissions"],
                    "category": "Security"
                },
                {
                    "question": "Explain database normalization. What are the different normal forms?",
                    "difficulty": "medium",
                    "keywords": ["normalization", "database", "normal forms", "redundancy", "integrity"],
                    "category": "Database"
                },
                {
                    "question": "What is middleware in web applications? Give examples.",
                    "difficulty": "easy",
                    "keywords": ["middleware", "request", "response", "processing", "express"],
                    "category": "Web Development"
                },
                {
                    "question": "Explain microservices architecture vs monolithic architecture.",
                    "difficulty": "medium",
                    "keywords": ["microservices", "monolithic", "architecture", "scalability", "deployment"],
                    "category": "Architecture"
                },
            ],
            "hr": [
                {
                    "question": "How do you decide whether to use frontend or backend solutions for a given feature?",
                    "difficulty": "medium",
                    "keywords": ["decision making", "trade-offs", "architecture", "analysis"],
                    "category": "Technical Decision"
                },
                {
                    "question": "Describe your approach to full-stack development. Frontend-first or backend-first?",
                    "difficulty": "easy",
                    "keywords": ["approach", "methodology", "workflow", "planning"],
                    "category": "Methodology"
                },
            ]
        }
    }
    
    # Generic questions applicable to all roles
    GENERIC_HR_QUESTIONS = [
        {
            "question": "Why do you want to work for this company?",
            "difficulty": "easy",
            "keywords": ["motivation", "interest", "company culture", "alignment"],
            "category": "Motivation"
        },
        {
            "question": "Where do you see yourself in 5 years?",
            "difficulty": "easy",
            "keywords": ["career goals", "ambition", "growth", "planning"],
            "category": "Career Goals"
        },
        {
            "question": "What are your greatest strengths and weaknesses?",
            "difficulty": "easy",
            "keywords": ["self-awareness", "strengths", "weaknesses", "improvement"],
            "category": "Self-Assessment"
        },
        {
            "question": "Why should we hire you over other candidates?",
            "difficulty": "medium",
            "keywords": ["unique value", "skills", "experience", "fit"],
            "category": "Value Proposition"
        },
    ]
    
    def generate_interview_questions(
        self,
        job_role: str,
        num_technical: int = 5,
        num_hr: int = 3,
        difficulty_filter: str = None
    ) -> List[Dict]:
        """
        Generate interview questions for a specific role
        
        Args:
            job_role: Target job role
            num_technical: Number of technical questions
            num_hr: Number of HR questions
            difficulty_filter: Optional difficulty filter (easy/medium/hard)
            
        Returns:
            List of question dictionaries
            
        Raises:
            InterviewGenerationError: If generation fails
        """
        try:
            logger.info(f"Generating interview questions for role: {job_role}")
            
            # Normalize role name
            role_key = job_role.lower().replace(" ", "_").replace("-", "_")
            
            # Get role-specific question bank
            role_questions = self.QUESTION_BANK.get(
                role_key,
                self.QUESTION_BANK["software_engineer"]  # Default fallback
            )
            
            # Filter and select technical questions
            technical_pool = role_questions.get("technical", [])
            if difficulty_filter:
                technical_pool = [
                    q for q in technical_pool
                    if q["difficulty"] == difficulty_filter
                ]
            
            # Ensure we have enough questions
            if len(technical_pool) < num_technical:
                # Add questions from general pool if needed
                technical_pool.extend(
                    self.QUESTION_BANK["software_engineer"]["technical"]
                )
            
            # Random selection without replacement
            technical_questions = random.sample(
                technical_pool,
                min(num_technical, len(technical_pool))
            )
            
            # Filter and select HR questions
            hr_pool = role_questions.get("hr", []) + self.GENERIC_HR_QUESTIONS
            if difficulty_filter:
                hr_pool = [
                    q for q in hr_pool
                    if q["difficulty"] == difficulty_filter
                ]
            
            hr_questions = random.sample(
                hr_pool,
                min(num_hr, len(hr_pool))
            )
            
            # Combine and format questions
            all_questions = []
            
            for idx, q in enumerate(technical_questions, 1):
                all_questions.append({
                    "question_id": f"tech_{idx}",
                    "question_type": "technical",
                    "question_text": q["question"],
                    "difficulty": q["difficulty"],
                    "category": q["category"],
                    "expected_keywords": q["keywords"],
                    "max_time_seconds": self._get_time_limit(q["difficulty"])
                })
            
            for idx, q in enumerate(hr_questions, 1):
                all_questions.append({
                    "question_id": f"hr_{idx}",
                    "question_type": "hr",
                    "question_text": q["question"],
                    "difficulty": q["difficulty"],
                    "category": q["category"],
                    "expected_keywords": q["keywords"],
                    "max_time_seconds": self._get_time_limit(q["difficulty"])
                })
            
            logger.info(f"Generated {len(all_questions)} questions")
            return all_questions
            
        except Exception as e:
            logger.error(f"Question generation failed: {str(e)}")
            raise InterviewGenerationError(str(e))
    
    def _get_time_limit(self, difficulty: str) -> int:
        """
        Get time limit based on difficulty
        
        Args:
            difficulty: Question difficulty
            
        Returns:
            Time limit in seconds
        """
        time_limits = {
            "easy": 180,      # 3 minutes
            "medium": 300,    # 5 minutes
            "hard": 420       # 7 minutes
        }
        
        return time_limits.get(difficulty, 300)
    
    def get_available_roles(self) -> List[str]:
        """
        Get list of available job roles
        
        Returns:
            List of role names
        """
        return [
            role.replace("_", " ").title()
            for role in self.QUESTION_BANK.keys()
        ]
    
    def get_question_statistics(self, job_role: str) -> Dict:
        """
        Get statistics about questions for a role
        
        Args:
            job_role: Target job role
            
        Returns:
            Dictionary with statistics
        """
        role_key = job_role.lower().replace(" ", "_")
        role_questions = self.QUESTION_BANK.get(
            role_key,
            self.QUESTION_BANK["software_engineer"]
        )
        
        technical = role_questions.get("technical", [])
        hr = role_questions.get("hr", [])
        
        return {
            "role": job_role,
            "total_technical": len(technical),
            "total_hr": len(hr) + len(self.GENERIC_HR_QUESTIONS),
            "difficulty_distribution": {
                "easy": len([q for q in technical if q["difficulty"] == "easy"]),
                "medium": len([q for q in technical if q["difficulty"] == "medium"]),
                "hard": len([q for q in technical if q["difficulty"] == "hard"])
            },
            "categories": list(set(q["category"] for q in technical + hr))
        }


# Global instance
question_generator = QuestionGenerator()
