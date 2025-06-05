import pdfplumber
import docx
import spacy
import re
from typing import Dict, Any, List
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file"""
    try:
        with pdfplumber.open(file) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    except Exception as e:
        raise Exception(f"PDF extraction error: {str(e)}")

def extract_text_from_docx(file) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        raise Exception(f"DOCX extraction error: {str(e)}")

def extract_text(file) -> str:
    """Determine file type and extract text accordingly"""
    if file.name.lower().endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.lower().endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")

def extract_education(text: str) -> str:
    """Extract education information from resume text"""
    patterns = [
        # FIX: add missing closing parenthesis at the end
        r"(?:education|academic background|qualifications)[\s\S]*?(?:(?:master|bachelor|ph\.?d|doctorate)[\s\S]*?(?:\d{4}[\s-]*(?:\d{4}|present)))",
        r"(master['s]?|bachelor['s]?|ph\.?d|doctorate)[\s\S]*?(?:in|of)[\s\S]*?[a-z]+(?:[\s,]*\d{4})",
        r"\b(university|college|institute)\b.*?\b(?:degree|diploma|certificate)\b"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return "Not specified"

def extract_experience(text: str) -> str:
    """Extract experience information from resume text"""
    # Look for years of experience
    exp_pattern = r"(?:\d+\+?[\s-]*(?:years?|yrs?)[\s-]*(?:experience))|(?:experience[\s\S]*?\d+\+?[\s-]*(?:years?|yrs?))"
    match = re.search(exp_pattern, text, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    
    # Look for job history section
    # FIX: add missing closing parenthesis at the end
    job_pattern = r"(?:experience|work history|employment)[\s\S]*?(?:(?:[a-z]+\s\d{4}[\s-]*(?:present|\d{4})))"
    match = re.search(job_pattern, text, re.IGNORECASE)
    if match:
        return f"Experience mentioned: {match.group(0)[:100]}..." if len(match.group(0)) > 100 else match.group(0).strip()
    
    return "Not specified"

def extract_info(text: str) -> Dict[str, Any]:
    """Extract structured information from resume text"""
    doc = nlp(text)
    
    # Email extraction
    email = next((ent.text for ent in doc.ents if ent.label_ == "EMAIL"), None)
    if not email:
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        email = emails[0] if emails else "Not found"

    # Phone extraction
    phone = next((ent.text for ent in doc.ents if ent.label_ == "PHONE"), None)
    if not phone:
        phones = re.findall(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        phone = phones[0] if phones else "Not found"

    # Skills extraction
    skill_set = [
        "python", "java", "react", "aws", "sql", "html", "css", 
        "machine learning", "ai", "tensorflow", "pytorch", "docker",
        "kubernetes", "git", "javascript", "typescript", "node.js",
        "data analysis", "pandas", "numpy", "scikit-learn", "flask",
        "django", "fastapi", "mongodb", "postgresql", "mysql",
        "big data", "hadoop", "spark", "tableau", "power bi"
    ]
    
    # Check for both individual words and phrases
    skills = []
    text_lower = text.lower()
    for skill in skill_set:
        if skill.lower() in text_lower:
            skills.append(skill.title())
    
    # Extract education and experience
    education = extract_education(text)
    experience = extract_experience(text)
    
    return {
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience
    }