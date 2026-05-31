"""
NLP Engine
Core natural language processing utilities using spaCy
"""

import spacy
from typing import List, Dict, Set, Tuple
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings
from app.core.exceptions import NLPModelError
from app.core.logging import get_logger

logger = get_logger(__name__)


class NLPEngine:
    """Singleton NLP engine using spaCy"""
    
    _instance = None
    _nlp = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize spaCy model"""
        if self._nlp is None:
            try:
                self._nlp = spacy.load(settings.SPACY_MODEL)
                logger.info(f"Loaded spaCy model: {settings.SPACY_MODEL}")
            except OSError:
                logger.error(f"spaCy model {settings.SPACY_MODEL} not found. Run: python -m spacy download {settings.SPACY_MODEL}")
                raise NLPModelError(
                    f"spaCy model not found. Install: python -m spacy download {settings.SPACY_MODEL}"
                )
    
    @property
    def nlp(self):
        """Get spaCy nlp instance"""
        return self._nlp
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of entity types and their values
        """
        doc = self._nlp(text)
        
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        
        # Remove duplicates while preserving order
        for key in entities:
            entities[key] = list(dict.fromkeys(entities[key]))
        
        return entities
    
    def extract_noun_phrases(self, text: str) -> List[str]:
        """
        Extract noun phrases (potential skills/technologies)
        
        Args:
            text: Input text
            
        Returns:
            List of noun phrases
        """
        doc = self._nlp(text)
        
        noun_phrases = []
        for chunk in doc.noun_chunks:
            # Filter out very short or common phrases
            if len(chunk.text) > 2 and not chunk.text.lower() in ['the', 'a', 'an']:
                noun_phrases.append(chunk.text)
        
        return list(set(noun_phrases))
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[Tuple[str, float]]:
        """
        Extract keywords using statistical methods
        
        Args:
            text: Input text
            top_n: Number of top keywords to return
            
        Returns:
            List of (keyword, score) tuples
        """
        doc = self._nlp(text)
        
        # Extract tokens that are not stop words or punctuation
        words = [
            token.lemma_.lower()
            for token in doc
            if not token.is_stop 
            and not token.is_punct 
            and len(token.text) > 2
            and token.is_alpha
        ]
        
        # Count frequencies
        word_freq = Counter(words)
        
        # Get top keywords
        top_keywords = word_freq.most_common(top_n)
        
        # Normalize scores
        max_freq = max(word_freq.values()) if word_freq else 1
        normalized = [(word, freq / max_freq) for word, freq in top_keywords]
        
        return normalized
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts using spaCy
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        doc1 = self._nlp(text1)
        doc2 = self._nlp(text2)
        
        return doc1.similarity(doc2)
    
    def compute_tfidf_similarity(
        self,
        text1: str,
        text2: str,
        use_bigrams: bool = False
    ) -> float:
        """
        Compute TF-IDF cosine similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            use_bigrams: Include bigrams in analysis
            
        Returns:
            Similarity score (0-1)
        """
        try:
            # Configure vectorizer
            ngram_range = (1, 2) if use_bigrams else (1, 1)
            vectorizer = TfidfVectorizer(
                ngram_range=ngram_range,
                stop_words='english',
                max_features=1000
            )
            
            # Compute TF-IDF vectors
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            
            # Compute cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"TF-IDF similarity computation failed: {str(e)}")
            return 0.0
    
    def extract_skill_candidates(self, text: str) -> Set[str]:
        """
        Extract potential skills from text using multiple strategies
        
        Args:
            text: Input text
            
        Returns:
            Set of skill candidates
        """
        doc = self._nlp(text)
        
        candidates = set()
        
        # Strategy 1: Noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text) > 2:
                candidates.add(chunk.text.lower())
        
        # Strategy 2: Proper nouns (ORG, PRODUCT)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                candidates.add(ent.text.lower())
        
        # Strategy 3: Technical terms (capitalized words/phrases)
        for token in doc:
            if token.is_alpha and len(token.text) > 2:
                # Capitalized non-sentence-starting words
                if token.text[0].isupper() and token.i > 0:
                    candidates.add(token.text)
        
        return candidates
    
    def tokenize_and_lemmatize(self, text: str) -> List[str]:
        """
        Tokenize and lemmatize text
        
        Args:
            text: Input text
            
        Returns:
            List of lemmatized tokens
        """
        doc = self._nlp(text)
        
        tokens = [
            token.lemma_.lower()
            for token in doc
            if not token.is_stop 
            and not token.is_punct 
            and token.is_alpha
        ]
        
        return tokens
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        doc = self._nlp(text)
        return [sent.text.strip() for sent in doc.sents]
    
    def detect_language_quality(self, text: str) -> Dict[str, any]:
        """
        Analyze language quality metrics
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with quality metrics
        """
        doc = self._nlp(text)
        
        total_tokens = len([t for t in doc if not t.is_space])
        total_sentences = len(list(doc.sents))
        
        # Calculate metrics
        avg_word_length = np.mean([len(token.text) for token in doc if token.is_alpha])
        avg_sentence_length = total_tokens / total_sentences if total_sentences > 0 else 0
        
        # Count parts of speech
        pos_counts = Counter([token.pos_ for token in doc])
        
        return {
            "total_words": total_tokens,
            "total_sentences": total_sentences,
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "unique_words": len(set([t.text.lower() for t in doc if t.is_alpha])),
            "pos_distribution": dict(pos_counts)
        }


# Global singleton instance
nlp_engine = NLPEngine()
