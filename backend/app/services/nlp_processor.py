# import re
# import json
# from typing import List, Dict, Set
# import spacy
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer

# class NLPProcessor:
#     """Classical NLP processing for resume and job text"""
    
#     def __init__(self):
#         # Load small spaCy model (CPU-friendly)
#         try:
#             self.nlp = spacy.load("en_core_web_sm")
#         except:
#             raise Exception("spaCy model not found. Run: python -m spacy download en_core_web_sm")
        
#         self.lemmatizer = WordNetLemmatizer()
#         self.stop_words = set(stopwords.words('english'))
        
#         # Common skills database (expandable)
#         self.skill_patterns = self._build_skill_patterns()
    
#     def _build_skill_patterns(self) -> List[str]:
#         """Build regex patterns for common skills"""
#         skills = [
#             # Programming Languages
#             r'\bpython\b', r'\bjava\b', r'\bjavascript\b', r'\btypescript\b',
#             r'\bc\+\+\b', r'\bc#\b', r'\bruby\b', r'\bphp\b', r'\bswift\b',
#             r'\bkotlin\b', r'\bgo\b', r'\brust\b', r'\br\b', r'\bscala\b',
            
#             # Web Technologies
#             r'\breact\b', r'\bangular\b', r'\bvue\.?js\b', r'\bnode\.?js\b',
#             r'\bexpress\b', r'\bdjango\b', r'\bflask\b', r'\bfastapi\b',
#             r'\bhtml5?\b', r'\bcss3?\b', r'\bsass\b', r'\btailwind\b',
            
#             # Databases
#             r'\bmysql\b', r'\bpostgresql\b', r'\bmongodb\b', r'\bredis\b',
#             r'\bsqlite\b', r'\boracle\b', r'\bsql\b', r'\bnosql\b',
            
#             # Cloud & DevOps
#             r'\baws\b', r'\bazure\b', r'\bgcp\b', r'\bdocker\b', r'\bkubernetes\b',
#             r'\bjenkins\b', r'\bgit\b', r'\bgithub\b', r'\bgitlab\b', r'\bci/cd\b',
            
#             # Data Science & ML
#             r'\bmachine\s+learning\b', r'\bdeep\s+learning\b', r'\bdata\s+science\b',
#             r'\bpandas\b', r'\bnumpy\b', r'\bscikit-learn\b', r'\btensorflow\b',
#             r'\bpytorch\b', r'\btableau\b', r'\bpower\s+bi\b',
            
#             # Other
#             r'\bagile\b', r'\bscrum\b', r'\bjira\b', r'\bapi\b', r'\brest\b',
#             r'\bgraphql\b', r'\bmicroservices\b', r'\btdd\b', r'\btest\s+automation\b'
#         ]
#         return skills
    
#     def preprocess_text(self, text: str) -> str:
#         """
#         Clean and preprocess text
#         - Lowercase
#         - Remove special characters
#         - Remove extra whitespace
#         """
#         # Lowercase
#         text = text.lower()
        
#         # Remove URLs
#         text = re.sub(r'http\S+|www\S+', '', text)
        
#         # Remove email addresses
#         text = re.sub(r'\S+@\S+', '', text)
        
#         # Remove special characters but keep spaces
#         text = re.sub(r'[^a-zA-Z0-9\s\+#\.]', ' ', text)
        
#         # Remove extra whitespace
#         text = re.sub(r'\s+', ' ', text).strip()
        
#         return text
    
#     def extract_skills(self, text: str) -> List[str]:
#         """
#         Extract skills using regex patterns
#         """
#         text_lower = text.lower()
#         skills_found = set()
        
#         for pattern in self.skill_patterns:
#             matches = re.finditer(pattern, text_lower)
#             for match in matches:
#                 skill = match.group().strip()
#                 # Clean up the skill name
#                 skill = re.sub(r'[^\w\s\+#\.]', '', skill)
#                 if len(skill) > 1:  # Avoid single characters
#                     skills_found.add(skill)
        
#         return sorted(list(skills_found))
    
#     def extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
#         """
#         Extract important keywords using:
#         1. Tokenization
#         2. Stop word removal
#         3. Lemmatization
#         4. Frequency analysis
#         """
#         # Preprocess
#         processed_text = self.preprocess_text(text)
        
#         # Tokenize
#         tokens = word_tokenize(processed_text)
        
#         # Remove stop words and short words
#         filtered_tokens = [
#             token for token in tokens 
#             if token not in self.stop_words and len(token) > 2
#         ]
        
#         # Lemmatize
#         lemmatized = [self.lemmatizer.lemmatize(token) for token in filtered_tokens]
        
#         # Count frequency
#         word_freq = {}
#         for word in lemmatized:
#             word_freq[word] = word_freq.get(word, 0) + 1
        
#         # Sort by frequency and get top N
#         sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
#         keywords = [word for word, freq in sorted_words[:top_n]]
        
#         return keywords
    
#     def extract_entities(self, text: str) -> Dict[str, List[str]]:
#         """
#         Extract named entities using spaCy
#         Returns: organizations, locations, etc.
#         """
#         doc = self.nlp(text[:1000000])  # Limit for performance
        
#         entities = {
#             'organizations': [],
#             'locations': [],
#             'persons': []
#         }
        
#         for ent in doc.ents:
#             if ent.label_ == 'ORG':
#                 entities['organizations'].append(ent.text)
#             elif ent.label_ == 'GPE':
#                 entities['locations'].append(ent.text)
#             elif ent.label_ == 'PERSON':
#                 entities['persons'].append(ent.text)
        
#         return entities





import re
import json
from typing import List, Dict

# ONLY technical skills - 85% threshold filtering
TECHNICAL_SKILLS = {
    # Programming Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "ruby", "go",
    "rust", "swift", "kotlin", "php", "scala", "r", "matlab", "perl",
    "bash", "powershell", "shell", "dart", "elixir", "haskell", "lua",

    # Frontend
    "react", "angular", "vue", "nextjs", "nuxtjs", "svelte", "jquery",
    "html", "css", "html5", "css3", "sass", "scss", "less", "tailwind",
    "bootstrap", "material-ui", "chakra-ui", "redux", "webpack", "vite",
    "typescript", "graphql", "rest", "restful",

    # Backend
    "nodejs", "express", "fastapi", "django", "flask", "spring", "laravel",
    "rails", "asp.net", "fastify", "nestjs", "strapi", "graphql",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle",
    "cassandra", "dynamodb", "elasticsearch", "neo4j", "firebase",
    "supabase", "prisma", "sequelize", "sqlalchemy",

    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "github actions", "gitlab ci", "circleci", "helm",
    "prometheus", "grafana", "datadog", "nginx", "apache",

    # ML/AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "keras", "huggingface", "opencv", "spark", "hadoop",
    "mlflow", "airflow", "dbt", "tableau", "power bi",

    # Tools & Others
    "git", "github", "gitlab", "jira", "confluence", "linux", "unix",
    "microservices", "ci/cd", "agile", "scrum", "kafka", "rabbitmq",
    "grpc", "websocket", "oauth", "jwt", "ssl", "tls",
    "figma", "sketch", "adobe xd", "selenium", "pytest", "jest",
    "solidity", "web3", "blockchain", "react native", "flutter",
    "unity", "unreal", "opengl", "vulkan", "cuda",
}

# Stop words to ignore
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "was", "are", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need", "dare",
    "ought", "used", "i", "me", "my", "myself", "we", "our", "you", "your",
    "he", "she", "it", "they", "them", "their", "this", "that", "these",
    "those", "which", "who", "whom", "whose", "what", "where", "when",
    "why", "how", "all", "both", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very", "just", "because", "as", "until", "while",
    "about", "against", "between", "into", "through", "during", "before",
    "after", "above", "below", "up", "down", "out", "off", "over",
    "under", "again", "then", "once", "here", "there", "when", "work",
    "working", "experience", "years", "year", "strong", "knowledge",
    "understanding", "familiarity", "ability", "skills", "skill",
    "preferred", "required", "plus", "bonus", "team", "cross", "functional",
    "looking", "seeking", "join", "build", "develop", "design", "implement",
    "manage", "lead", "create", "ensure", "provide", "support", "use",
    "using", "used", "like", "including", "including", "etc", "new",
    "also", "well", "across", "within", "without", "related", "based",
}

def extract_skills_from_text(text: str) -> List[str]:
    """Extract ONLY technical skills from resume text"""
    if not text:
        return []
    
    text_lower = text.lower()
    found_skills = set()
    
    # Check multi-word skills first
    multi_word_skills = [s for s in TECHNICAL_SKILLS if ' ' in s]
    for skill in multi_word_skills:
        if skill in text_lower:
            found_skills.add(skill)
    
    # Check single-word skills
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.-]*\b', text_lower)
    for word in words:
        if word in TECHNICAL_SKILLS and len(word) > 1:
            found_skills.add(word)
    
    return sorted(list(found_skills))

def extract_technical_keywords(text: str, max_keywords: int = 20) -> List[str]:
    """Extract technical keywords with 85% threshold filtering"""
    if not text:
        return []
    
    text_lower = text.lower()
    
    # First get all skills
    skills = extract_skills_from_text(text)
    
    # Get word frequency for technical terms only
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.-]*\b', text_lower)
    
    word_freq = {}
    for word in words:
        # ONLY count if it's a technical term or skill
        if (word not in STOP_WORDS 
            and len(word) > 2 
            and word in TECHNICAL_SKILLS):
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Combine skills and frequent technical words
    keywords = list(set(skills + [w for w, _ in sorted_words[:max_keywords]]))
    
    return keywords[:max_keywords]

def calculate_skill_match_score(resume_skills: List[str], job_text: str) -> float:
    """
    Calculate match score with 85% technical skill threshold.
    Returns score between 0 and 1.
    Only counts technical skills, ignores non-technical keywords.
    """
    if not resume_skills or not job_text:
        return 0.0
    
    job_text_lower = job_text.lower()
    
    # Extract technical skills from job
    job_skills = extract_skills_from_text(job_text)
    
    if not job_skills:
        return 0.0
    
    # Calculate overlap
    resume_skills_set = set(s.lower() for s in resume_skills)
    job_skills_set = set(s.lower() for s in job_skills)
    
    matched = resume_skills_set & job_skills_set
    
    # Score = matched / total job skills required
    if len(job_skills_set) == 0:
        return 0.0
    
    score = len(matched) / len(job_skills_set)
    
    # Apply 85% threshold boost - if score >= 0.85, boost it
    if score >= 0.85:
        score = min(score * 1.1, 1.0)
    
    return round(score, 4)

def process_resume_text(raw_text: str) -> Dict:
    """
    Process resume and extract ONLY technical information.
    Filters out non-technical keywords.
    """
    if not raw_text:
        return {"skills": [], "keywords": [], "processed_text": ""}
    
    # Extract skills
    skills = extract_skills_from_text(raw_text)
    
    # Extract technical keywords only
    keywords = extract_technical_keywords(raw_text)
    
    # Clean text - remove common non-technical words for better TF-IDF
    words = raw_text.lower().split()
    technical_words = []
    for word in words:
        clean_word = re.sub(r'[^a-zA-Z0-9+#.-]', '', word)
        if (clean_word not in STOP_WORDS 
            and len(clean_word) > 2):
            technical_words.append(clean_word)
    
    processed_text = ' '.join(technical_words)
    
    return {
        "skills": skills,
        "keywords": keywords,
        "processed_text": processed_text
    }