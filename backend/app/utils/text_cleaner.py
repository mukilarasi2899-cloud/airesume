"""
Text Cleaning and Preprocessing Utilities
"""

import re
from typing import List
from textblob import TextBlob

from app.core.logging import get_logger

logger = get_logger(__name__)


class TextCleaner:
    """Text preprocessing and cleaning utilities"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\-\@\+\#\(\)]', '', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    @staticmethod
    def remove_emails(text: str) -> str:
        """Remove email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.sub(email_pattern, '', text)
    
    @staticmethod
    def remove_phone_numbers(text: str) -> str:
        """Remove phone numbers from text"""
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}'
        return re.sub(phone_pattern, '', text)
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """
        Extract email addresses from text
        
        Args:
            text: Input text
            
        Returns:
            List of email addresses
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """
        Extract phone numbers from text
        
        Args:
            text: Input text
            
        Returns:
            List of phone numbers
        """
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}'
        return re.findall(phone_pattern, text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        Extract URLs from text
        
        Args:
            text: Input text
            
        Returns:
            List of URLs
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    @staticmethod
    def tokenize_sentences(text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def tokenize_words(text: str) -> List[str]:
        """
        Split text into words
        
        Args:
            text: Input text
            
        Returns:
            List of words
        """
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    @staticmethod
    def correct_spelling(text: str) -> str:
        """
        Correct spelling using TextBlob
        
        Args:
            text: Input text
            
        Returns:
            Text with corrected spelling
        """
        try:
            blob = TextBlob(text)
            return str(blob.correct())
        except Exception as e:
            logger.warning(f"Spelling correction failed: {str(e)}")
            return text
    
    @staticmethod
    def detect_grammar_issues(text: str) -> List[str]:
        """
        Detect basic grammar issues
        
        Args:
            text: Input text
            
        Returns:
            List of detected issues
        """
        issues = []
        
        # Check for repeated words
        words = text.split()
        for i in range(len(words) - 1):
            if words[i].lower() == words[i + 1].lower():
                issues.append(f"Repeated word: '{words[i]}'")
        
        # Check for multiple spaces
        if '  ' in text:
            issues.append("Multiple consecutive spaces detected")
        
        # Check for missing capitalization at sentence start
        sentences = TextCleaner.tokenize_sentences(text)
        for sentence in sentences:
            if sentence and not sentence[0].isupper():
                issues.append(f"Sentence should start with capital: '{sentence[:30]}...'")
        
        return issues
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace in text
        
        Args:
            text: Input text
            
        Returns:
            Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace multiple newlines with double newline
        text = re.sub(r'\n\n+', '\n\n', text)
        
        # Remove trailing/leading whitespace
        return text.strip()
    
    @staticmethod
    def extract_years(text: str) -> List[int]:
        """
        Extract years from text (useful for education/experience dates)
        
        Args:
            text: Input text
            
        Returns:
            List of years found
        """
        # Match 4-digit years between 1950 and 2050
        year_pattern = r'\b(19[5-9]\d|20[0-5]\d)\b'
        years = re.findall(year_pattern, text)
        return sorted([int(year) for year in years])
