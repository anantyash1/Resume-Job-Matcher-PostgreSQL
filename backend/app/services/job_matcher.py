# import json
# from typing import List, Dict, Tuple
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# class JobMatcher:
#     """
#     TF-IDF based job matching engine
#     Uses classical cosine similarity for explainable results
#     """
    
#     def __init__(self):
#         self.vectorizer = TfidfVectorizer(
#             max_features=500,  # Limit features for performance
#             ngram_range=(1, 2),  # Unigrams and bigrams
#             stop_words='english'
#         )
    
#     def match_jobs(
#         self, 
#         resume_text: str,
#         resume_skills: List[str],
#         jobs: List[Dict],
#         top_n: int = 10
#     ) -> List[Dict]:
#         """
#         Match resume to jobs using TF-IDF and cosine similarity
        
#         Args:
#             resume_text: Preprocessed resume text
#             resume_skills: Extracted skills from resume
#             jobs: List of job dictionaries with 'description' field
#             top_n: Number of top matches to return
            
#         Returns:
#             List of job matches with similarity scores and matched skills
#         """
#         if not jobs:
#             return []
        
#         # Prepare job texts (description + requirements)
#         job_texts = []
#         for job in jobs:
#             job_text = job.get('description', '') + ' ' + job.get('requirements', '')
#             job_texts.append(job_text)
        
#         # Add resume text to corpus
#         all_texts = [resume_text] + job_texts
        
#         try:
#             # Fit TF-IDF vectorizer
#             tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            
#             # Get resume vector (first one)
#             resume_vector = tfidf_matrix[0:1]
            
#             # Get job vectors
#             job_vectors = tfidf_matrix[1:]
            
#             # Calculate cosine similarity
#             similarities = cosine_similarity(resume_vector, job_vectors)[0]
            
#             # Create results with similarity scores
#             results = []
#             for idx, job in enumerate(jobs):
#                 similarity_score = float(similarities[idx])
                
#                 # Find matched skills
#                 matched_skills = self._find_matched_skills(
#                     resume_skills,
#                     job.get('description', '') + ' ' + job.get('requirements', '')
#                 )
                
#                 results.append({
#                     'job': job,
#                     'similarity_score': round(similarity_score, 4),
#                     'matched_skills': matched_skills
#                 })
            
#             # Sort by similarity score
#             results.sort(key=lambda x: x['similarity_score'], reverse=True)
            
#             return results[:top_n]
            
#         except Exception as e:
#             print(f"Error in job matching: {str(e)}")
#             return []
    
#     def _find_matched_skills(self, resume_skills: List[str], job_text: str) -> List[str]:
#         """
#         Find which resume skills appear in the job description
#         """
#         job_text_lower = job_text.lower()
#         matched = []
        
#         for skill in resume_skills:
#             if skill.lower() in job_text_lower:
#                 matched.append(skill)
        
#         return matched
    
#     def explain_match(self, resume_text: str, job_text: str, top_terms: int = 10) -> List[Tuple[str, float]]:
#         """
#         Explain why a job matched by showing top contributing terms
#         """
#         try:
#             # Vectorize both texts
#             tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_text])
            
#             # Get feature names
#             feature_names = self.vectorizer.get_feature_names_out()
            
#             # Get TF-IDF scores for resume
#             resume_scores = tfidf_matrix[0].toarray()[0]
            
#             # Get indices of top scores
#             top_indices = resume_scores.argsort()[-top_terms:][::-1]
            
#             # Return terms and their scores
#             explanations = [
#                 (feature_names[idx], resume_scores[idx])
#                 for idx in top_indices
#                 if resume_scores[idx] > 0
#             ]
            
#             return explanations
            
#         except Exception as e:
#             print(f"Error explaining match: {str(e)}")
#             return []



import json
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .nlp_processor import (
    extract_skills_from_text, 
    calculate_skill_match_score,
    TECHNICAL_SKILLS,
    STOP_WORDS
)

class JobMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words=list(STOP_WORDS),  # Use our technical stop words
            ngram_range=(1, 2),
            min_df=1
        )
    
    def match_jobs(
        self, 
        resume_text: str,
        resume_skills: List[str],
        jobs: List[Dict],
        top_n: int = 10,
        min_score: float = 0.0  # Minimum score threshold
    ) -> List[Dict]:
        """
        Match jobs using TF-IDF + Technical Skill matching.
        85% weight on technical skills, 15% on text similarity.
        """
        if not jobs or not resume_text:
            return []
        
        results = []
        
        for job in jobs:
            job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('requirements', '')}"
            
            # Calculate TF-IDF similarity
            try:
                tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_text])
                tfidf_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            except Exception:
                tfidf_score = 0.0
            
            # Calculate technical skill match score (85% threshold)
            skill_score = calculate_skill_match_score(resume_skills, job_text)
            
            # Get job skills for this job
            job_skills = extract_skills_from_text(job_text)
            
            # Find matched skills
            resume_skills_set = set(s.lower() for s in resume_skills)
            job_skills_set = set(s.lower() for s in job_skills)
            matched_skills = list(resume_skills_set & job_skills_set)
            
            # Combined score: 85% skill match + 15% text similarity
            combined_score = (skill_score * 0.85) + (tfidf_score * 0.15)
            combined_score = round(min(combined_score, 1.0), 4)
            
            # Only include if above minimum score
            if combined_score >= min_score:
                results.append({
                    'job': job,
                    'similarity_score': combined_score,
                    'matched_skills': matched_skills,
                    'skill_score': skill_score,
                    'tfidf_score': float(tfidf_score)
                })
        
        # Sort by combined score descending
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return results[:top_n]