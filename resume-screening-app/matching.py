from typing import cast
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import re
from utils import preprocess_text

def compute_match(resume_text: str, jd_text: str) -> float:
    """
    Compute match percentage between resume and job description
    using TF-IDF and cosine similarity with keyword bonuses
    """
    # Preprocess texts
    resume_processed = preprocess_text(resume_text)
    jd_processed = preprocess_text(jd_text)
    
    # Create TF-IDF vectors with n-grams
    vectorizer = TfidfVectorizer(
        stop_words='english', 
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.9
    )
    
    # Cast the result of fit_transform to csr_matrix
    tfidf_matrix = cast(csr_matrix, vectorizer.fit_transform([resume_processed, jd_processed]))
    
    # Convert to dense arrays for similarity calculation
    dense_matrix = tfidf_matrix.toarray()
    resume_vec = dense_matrix[0].reshape(1, -1)
    jd_vec = dense_matrix[1].reshape(1, -1)
    
    # Calculate base cosine similarity
    similarity = cosine_similarity(resume_vec, jd_vec)
    base_score = float(similarity[0][0]) * 100
    
    # Extract important keywords from JD
    keywords = set()
    for word in jd_processed.split():
        if len(word) > 3 and word not in vectorizer.get_stop_words():
            keywords.add(word.lower())
    
    # Calculate keyword match bonus (up to 20 points)
    keyword_bonus = 0
    matched_keywords = []
    resume_words = set(resume_processed.lower().split())
    
    for keyword in keywords:
        if keyword in resume_words:
            matched_keywords.append(keyword)
            keyword_bonus += 2  # 2 points per matched keyword
    
    # Cap the bonus at 20 points
    keyword_bonus = min(keyword_bonus, 20)
    
    # Calculate final score (base + bonus, capped at 100)
    final_score = min(base_score + keyword_bonus, 100)
    
    return round(final_score, 2)
