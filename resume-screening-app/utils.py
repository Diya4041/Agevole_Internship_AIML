import base64
from typing import Optional
import re
import streamlit as st

def show_pdf(file):
    """Display PDF in Streamlit app"""
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    return st.markdown(pdf_display, unsafe_allow_html=True)

def preprocess_text(text: str) -> str:
    """Clean and preprocess text for analysis"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove special characters except basic punctuation
    text = re.sub(r'[^\w\s.,;:!?\'"-]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def validate_email(email: str) -> Optional[str]:
    """Validate email format"""
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    match = re.fullmatch(pattern, email)
    return email if match else None

def validate_phone(phone: str) -> Optional[str]:
    """Validate phone number format"""
    pattern = r"^\+?\(?\d{3}\)?[-\s.]?\d{3}[-\s.]?\d{4,6}$"
    match = re.fullmatch(pattern, phone)
    return phone if match else None