# # app.py
# import streamlit as st
# import tempfile
# from utils import extract_text_from_file
# from model import compute_similarity
# from classifier import predict_category

# st.title("📄 AI Resume Matcher & Classifier")

# jd = st.text_area("Paste Job Description")

# uploaded_files = st.file_uploader("Upload resumes (PDF/DOCX)", accept_multiple_files=True)

# if st.button("Rank Resumes") and jd and uploaded_files:
#     resumes = []
#     names = []
#     for file in uploaded_files:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=file.name[-5:]) as tmp:
#             tmp.write(file.read())
#             text = extract_text_from_file(tmp.name)
#             resumes.append(text)
#             names.append(file.name)

#     sims = compute_similarity(jd, resumes)

#     st.subheader("🔍 Ranked Resumes")
#     for i, (name, text, sim) in enumerate(sorted(zip(names, resumes, sims), key=lambda x: x[2], reverse=True)):
#         category = predict_category(text)
#         st.markdown(f"""
#         **{i+1}. {name}**  
#         - Similarity Score: `{sim:.4f}`  
#         - Predicted Role: `{category}`  
#         """)

# app.py
import streamlit as st
import tempfile
import pandas as pd
from utils import extract_text_from_file
from model import get_similarity_scores, load_classifier

st.set_page_config(page_title="AI Resume Matcher", layout="wide")
st.title("🤖 AI-Powered Resume Matcher")

# Upload job description
jd = st.text_area("Paste Job Description")

# Upload resumes
uploaded_files = st.file_uploader("Upload Resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

# Load classifier
clf = load_classifier()

if st.button("Match & Classify") and jd and uploaded_files:
    texts = []
    names = []

    for f in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f.name[-5:]) as tmp:
            tmp.write(f.read())
            text = extract_text_from_file(tmp.name)
            texts.append(text)
            names.append(f.name)

    # Similarity scores
    sims = get_similarity_scores(jd, texts)
    
    st.subheader("📊 Ranked Results:")
    results = sorted(zip(names, texts, sims), key=lambda x: x[2], reverse=True)
    for i, (name, text, score) in enumerate(results):
        category = clf.predict([text])[0]
        st.markdown(f"""
        **{i+1}. {name}**
        - Similarity Score: `{score:.4f}`
        - Predicted Category: `{category}`
        """)
