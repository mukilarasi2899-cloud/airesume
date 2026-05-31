"""
Resume Parser
Extracts structured information from resume text
"""

import re
from typing import Dict, List, Optional
from datetime import datetime

from app.services.nlp_engine import nlp_engine
from app.services.skill_extractor import skill_extractor
from app.utils.text_cleaner import TextCleaner
from app.core.exceptions import ResumeParsingError
from app.core.logging import get_logger

logger = get_logger(__name__)


class ResumeParser:
    """Parse resume and extract structured information"""
    
    # Section headers commonly found in resumes
    SECTION_PATTERNS = {
        "education": r"education|academic|qualification|degree",
        "experience": r"experience|employment|work history|professional background",
        "projects": r"projects?|portfolio",
        "skills": r"skills?|technical skills|competencies|expertise",
        "certifications": r"certifications?|certificates?|licenses?",
        "summary": r"summary|objective|profile|about",
        "achievements": r"achievements?|accomplishments?|awards?",
    }
    
    # Education degree patterns
    DEGREE_PATTERNS = [
        r"ph\.?d\.?", r"doctorate", r"doctor of",
        r"master'?s?", r"m\.?s\.?", r"m\.?tech", r"m\.?b\.?a\.?",
        r"bachelor'?s?", r"b\.?s\.?", r"b\.?tech", r"b\.?e\.?", r"b\.?a\.?",
        r"associate", r"diploma", r"certificate", r"degree"
    ]
    
    def __init__(self):
        """Initialize resume parser"""
        self.text_cleaner = TextCleaner()
    
    def parse(self, resume_text: str) -> Dict:
        """
        Parse resume and extract all information
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Structured resume data
            
        Raises:
            ResumeParsingError: If parsing fails
        """
        try:
            logger.info("Starting resume parsing")
            
            # Clean text
            cleaned_text = self.text_cleaner.clean_text(resume_text)
            
            # Extract contact information
            contact_info = self._extract_contact_info(resume_text)
            
            # Identify sections
            sections = self._identify_sections(cleaned_text)
            
            # Extract education
            education = self._extract_education(
                sections.get("education", ""),
                cleaned_text
            )
            
            # Extract experience
            experience = self._extract_experience(
                sections.get("experience", ""),
                cleaned_text
            )
            
            # Extract skills
            skills = skill_extractor.extract_skills(cleaned_text)
            skill_clusters = skill_extractor.cluster_skills(skills["all_skills"])
            
            # Extract projects
            projects = self._extract_projects(
                sections.get("projects", ""),
                cleaned_text
            )
            
            # Extract certifications
            certifications = self._extract_certifications(
                sections.get("certifications", ""),
                cleaned_text
            )
            
            # Extract summary
            summary = self._extract_summary(
                sections.get("summary", ""),
                cleaned_text
            )
            
            # Analyze language quality
            language_quality = nlp_engine.detect_language_quality(cleaned_text)
            
            # Calculate experience years
            total_experience_years = self._calculate_total_experience(experience)
            
            parsed_data = {
                "contact_info": contact_info,
                "summary": summary,
                "education": education,
                "experience": experience,
                "skills": skills,
                "skill_clusters": skill_clusters,
                "projects": projects,
                "certifications": certifications,
                "total_experience_years": total_experience_years,
                "language_quality": language_quality,
                "parsing_metadata": {
                    "parsed_at": datetime.utcnow().isoformat(),
                    "total_characters": len(cleaned_text),
                    "sections_found": list(sections.keys())
                }
            }
            
            logger.info("Resume parsing completed successfully")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Resume parsing failed: {str(e)}")
            raise ResumeParsingError(str(e))
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """
        Identify and extract sections from resume
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary of section names and their content
        """
        sections = {}
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            is_header = False
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line_lower) and len(line.split()) < 5:
                    # Save previous section
                    if current_section and section_content:
                        sections[current_section] = '\n'.join(section_content)
                    
                    # Start new section
                    current_section = section_name
                    section_content = []
                    is_header = True
                    break
            
            if not is_header and current_section:
                section_content.append(line)
        
        # Save last section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
    def _extract_contact_info(self, text: str) -> Dict[str, any]:
        """
        Extract contact information
        
        Args:
            text: Resume text
            
        Returns:
            Contact information dictionary
        """
        contact = {
            "emails": self.text_cleaner.extract_emails(text),
            "phones": self.text_cleaner.extract_phone_numbers(text),
            "urls": self.text_cleaner.extract_urls(text)
        }
        
        # Extract LinkedIn
        linkedin = [url for url in contact["urls"] if "linkedin.com" in url.lower()]
        contact["linkedin"] = linkedin[0] if linkedin else None
        
        # Extract GitHub
        github = [url for url in contact["urls"] if "github.com" in url.lower()]
        contact["github"] = github[0] if github else None
        
        return contact
    
    def _extract_education(self, section_text: str, full_text: str) -> List[Dict]:
        """
        Extract education information
        
        Args:
            section_text: Education section text
            full_text: Full resume text
            
        Returns:
            List of education entries
        """
        education_list = []
        text_to_parse = section_text if section_text else full_text
        
        # Find degree patterns
        for degree_pattern in self.DEGREE_PATTERNS:
            pattern = r'(.{0,100}' + degree_pattern + r'.{0,100})'
            matches = re.finditer(pattern, text_to_parse, re.IGNORECASE)
            
            for match in matches:
                context = match.group(1)
                
                # Extract degree, institution, and year
                entry = {
                    "degree": self._extract_degree_name(context),
                    "institution": self._extract_institution(context),
                    "year": self._extract_year(context),
                    "field": self._extract_field_of_study(context)
                }
                
                # Avoid duplicates
                if entry not in education_list and entry["degree"]:
                    education_list.append(entry)
        
        return education_list
    
    def _extract_degree_name(self, text: str) -> Optional[str]:
        """Extract degree name from text"""
        for pattern in self.DEGREE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Expand context around match
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 30)
                degree_text = text[start:end].strip()
                
                # Clean and return
                degree_text = re.sub(r'\s+', ' ', degree_text)
                return degree_text[:100]  # Limit length
        return None
    
    def _extract_institution(self, text: str) -> Optional[str]:
        """Extract institution name from text"""
        doc = nlp_engine.nlp(text)
        
        # Look for ORG entities (institutions)
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                return ent.text
        
        return None
    
    def _extract_year(self, text: str) -> Optional[int]:
        """Extract year from text"""
        years = self.text_cleaner.extract_years(text)
        return years[-1] if years else None  # Return most recent year
    
    def _extract_field_of_study(self, text: str) -> Optional[str]:
        """Extract field of study from text"""
        # Common field patterns
        field_patterns = [
            r"in\s+([A-Z][a-zA-Z\s]+)",
            r"of\s+([A-Z][a-zA-Z\s]+)",
            r",\s+([A-Z][a-zA-Z\s]+)"
        ]
        
        for pattern in field_patterns:
            match = re.search(pattern, text)
            if match:
                field = match.group(1).strip()
                if 3 < len(field) < 50:
                    return field
        
        return None
    
    def _extract_experience(self, section_text: str, full_text: str) -> List[Dict]:
        """
        Extract work experience
        
        Args:
            section_text: Experience section text
            full_text: Full resume text
            
        Returns:
            List of experience entries
        """
        experience_list = []
        text_to_parse = section_text if section_text else full_text
        
        # Split by common delimiters
        entries = re.split(r'\n\n+', text_to_parse)
        
        for entry in entries:
            if len(entry.strip()) < 20:
                continue
            
            exp_entry = {
                "title": self._extract_job_title(entry),
                "company": self._extract_company(entry),
                "duration": self._extract_duration(entry),
                "description": self._extract_job_description(entry),
                "years": self._extract_years_from_duration(entry)
            }
            
            if exp_entry["title"] or exp_entry["company"]:
                experience_list.append(exp_entry)
        
        return experience_list[:10]  # Limit to reasonable number
    
    def _extract_job_title(self, text: str) -> Optional[str]:
        """Extract job title from experience entry"""
        # Usually first line or first significant text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Look for title patterns
            title_patterns = [
                r"^([A-Z][a-zA-Z\s]+(?:Engineer|Developer|Manager|Analyst|Scientist|Designer|Architect))",
                r"^([A-Z][a-zA-Z\s]{5,50})"
            ]
            
            for pattern in title_patterns:
                match = re.search(pattern, lines[0])
                if match:
                    return match.group(1).strip()
        
        return None
    
    def _extract_company(self, text: str) -> Optional[str]:
        """Extract company name from experience entry"""
        doc = nlp_engine.nlp(text[:200])  # First 200 chars usually have company
        
        # Look for ORG entities
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                return ent.text
        
        return None
    
    def _extract_duration(self, text: str) -> Optional[str]:
        """Extract duration from experience entry"""
        # Look for date patterns
        patterns = [
            r"(\d{4}\s*[-–]\s*\d{4})",
            r"(\d{4}\s*[-–]\s*Present)",
            r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*[-–]\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}))"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_years_from_duration(self, text: str) -> float:
        """Calculate years from duration text"""
        years = self.text_cleaner.extract_years(text)
        
        if len(years) >= 2:
            return round(years[-1] - years[0], 1)
        elif "present" in text.lower() and years:
            current_year = datetime.now().year
            return round(current_year - years[0], 1)
        
        return 0.0
    
    def _extract_job_description(self, text: str) -> str:
        """Extract job description"""
        # Remove title and company (usually first 1-2 lines)
        lines = text.split('\n')
        description_lines = lines[2:] if len(lines) > 2 else lines
        
        description = '\n'.join(description_lines).strip()
        return description[:500]  # Limit length
    
    def _extract_projects(self, section_text: str, full_text: str) -> List[Dict]:
        """Extract project information"""
        projects = []
        text_to_parse = section_text if section_text else ""
        
        if not text_to_parse:
            return projects
        
        # Split by project entries
        entries = re.split(r'\n\n+', text_to_parse)
        
        for entry in entries:
            if len(entry.strip()) < 20:
                continue
            
            project = {
                "name": self._extract_project_name(entry),
                "description": entry.strip()[:300],
                "technologies": skill_extractor.extract_skills(entry)["technical_skills"]
            }
            
            if project["name"]:
                projects.append(project)
        
        return projects[:10]
    
    def _extract_project_name(self, text: str) -> Optional[str]:
        """Extract project name (usually first line)"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return lines[0] if lines else None
    
    def _extract_certifications(self, section_text: str, full_text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        text_to_parse = section_text if section_text else ""
        
        if not text_to_parse:
            return certifications
        
        # Split by lines or bullets
        lines = text_to_parse.split('\n')
        
        for line in lines:
            line = line.strip()
            # Remove bullet points
            line = re.sub(r'^[•\-\*]\s*', '', line)
            
            if 5 < len(line) < 200:
                certifications.append(line)
        
        return certifications
    
    def _extract_summary(self, section_text: str, full_text: str) -> str:
        """Extract professional summary"""
        if section_text:
            return section_text.strip()[:500]
        
        # Try to extract from beginning of resume
        lines = full_text.split('\n')
        summary_lines = []
        
        for line in lines[:10]:  # Check first 10 lines
            if len(line.strip()) > 50:  # Likely a summary sentence
                summary_lines.append(line.strip())
        
        return ' '.join(summary_lines)[:500] if summary_lines else ""
    
    def _calculate_total_experience(self, experience: List[Dict]) -> float:
        """Calculate total years of experience"""
        total_years = sum(exp.get("years", 0) for exp in experience)
        return round(total_years, 1)
    
    def generate_resume_summary(self, parsed_data: Dict) -> str:
        """
        Generate a summary of the parsed resume
        
        Args:
            parsed_data: Parsed resume data
            
        Returns:
            Human-readable summary
        """
        skills = parsed_data.get("skills", {}).get("all_skills", [])
        experience = parsed_data.get("total_experience_years", 0)
        education = parsed_data.get("education", [])
        
        summary = f"Resume Summary:\n"
        summary += f"- Total Experience: {experience} years\n"
        summary += f"- Education: {len(education)} entries\n"
        summary += f"- Skills: {len(skills)} identified\n"
        summary += f"- Top Skills: {', '.join(skills[:10])}\n"
        
        return summary


# Global instance
resume_parser = ResumeParser()
