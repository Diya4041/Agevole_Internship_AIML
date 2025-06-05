import streamlit as st
import pandas as pd
import time
import json
import os
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv

# This is the only set_page_config call needed
st.set_page_config(
    page_title="AI Resume Screening Pro",
    page_icon="📄",
    layout="wide",
    menu_items={
        'Get Help': 'https://example.com',
        'Report a bug': "https://example.com",
        'About': "# Professional Resume Screening Tool"
    }
)

# Then load environment variables and import local modules
load_dotenv()

try:
    from parser import extract_text, extract_info
    from matching import compute_match
    from utils import show_pdf
    from firebase_auth import firebase_auth
except ImportError as e:
    st.error(f"Missing required modules: {str(e)}")
    st.stop()

# Remove the duplicate set_page_config call that was here

# Custom CSS for styling
st.markdown("""
<style>
    :root {
        --primary: #4f46e5;
        --secondary: #f9fafb;
        --accent: #10b981;
        --text: #1f2937;
        --error: #ef4444;
        --warning: #f59e0b;
    }
    .stApp {
        background-color: #f8fafc;
    }
    .stProgress > div > div > div > div {
        background-color: var(--accent);
    }
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: none;
        font-weight: 500;
        transition: all 0.2s;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .header-title {
        background: linear-gradient(90deg, var(--primary), #7c3aed);
        color: white;
        padding: 20px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
        text-align: center;
        font-weight: 700;
        font-size: 2.25rem;
    }
    .card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .error-message {
        color: var(--error);
        background-color: #fef2f2;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid var(--error);
        margin-bottom: 15px;
    }
    a {
        color: var(--primary);
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'auth_page' not in st.session_state:
    st.session_state.auth_page = 'login'
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'results' not in st.session_state:
    st.session_state.results = None

# --- Utility functions ---

def generate_report(df: pd.DataFrame, jd_title: str, jd_text: str) -> str:
    """Generate a detailed screening report as a string."""
    report = []
    report.append(f"AI Resume Screening Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("\n" + "="*80 + "\n")
    report.append(f"Job Title: {jd_title}")
    report.append(f"Job Description: {jd_text}")
    report.append(f"Total Candidates: {len(df)}")
    report.append(f"Average Match Score: {df['Match %'].mean():.1f}%")
    report.append("\n" + "="*80 + "\n")

    for _, row in df.iterrows():
        report.append(f"\nCandidate: {row['Candidate']}")
        report.append(f"Match Score: {row['Match %']}% - {row['Recommendation']}")
        report.append(f"Contact: {row['Email']} | {row['Phone']}")
        report.append(f"Skills: {row['Skills']}")
        report.append(f"Experience: {row['Experience']}")
        report.append(f"Education: {row['Education']}")
        report.append("-"*60)

    return "\n".join(report)

def load_job_descriptions() -> Dict[str, str]:
    """Load job descriptions from JSON file or return defaults."""
    try:
        if os.path.exists("job_descriptions.json"):
            with open("job_descriptions.json", "r") as f:
                return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # Default job descriptions fallback
    return {
        "Data Scientist": "Looking for a candidate with expertise in ML, Python, data visualization, and cloud.",
        "Frontend Developer": "Must be skilled in React, CSS, HTML, and responsive UI design.",
        "DevOps Engineer": "Strong knowledge of Docker, Kubernetes, AWS, and CI/CD pipelines."
    }

def save_job_descriptions(jd_options: Dict[str, str]):
    """Save job descriptions to JSON file."""
    with open("job_descriptions.json", "w") as f:
        json.dump(jd_options, f, indent=4)

def process_resumes(uploaded_files, selected_jd_text):
    """Process uploaded resumes and compute match scores."""
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, file in enumerate(uploaded_files):
        status_text.markdown(f"<div class='card'>Processing <b>{i+1}/{len(uploaded_files)}</b>: {file.name}</div>",
                             unsafe_allow_html=True)
        try:
            text = extract_text(file)
            info = extract_info(text)
            match_score = compute_match(text, selected_jd_text)

            results.append({
                "Candidate": file.name,
                "Match %": round(match_score, 1),
                "Email": info.get("email", "Not found"),
                "Phone": info.get("phone", "Not found"),
                "Skills": ", ".join(info.get("skills", [])) if info.get("skills") else "Not found",
                "Experience": info.get("experience", "Not specified"),
                "Education": info.get("education", "Not specified"),
                "Recommendation": "⭐ Strong Match" if match_score >= 85
                                  else "👍 Good Fit" if match_score >= 70
                                  else "🤔 Needs Review",
                "Raw Text": text  # Store for preview if needed
            })

            progress_bar.progress((i + 1) / len(uploaded_files))
            time.sleep(0.1)  # Simulate processing delay

        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")

    status_text.empty()
    return results

# --- Authentication pages ---

def login_page():
    st.markdown("<div class='header-title'>🔐 Professional Resume Screening</div>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/3209/3209269.png", width=150)
        with col2:
            st.header("Sign In to Your Account")
            with st.form("login_form"):
                email = st.text_input("Email Address", placeholder="your@company.com")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Sign In", use_container_width=True):
                    if firebase_auth.login_with_email_and_password(email, password):
                        st.session_state.auth_page = 'app'
                        st.rerun()
                    else:
                        st.error("Invalid email or password")

            st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <p>Don't have an account? <a href="#" onclick="window.parent.document.querySelector('[data-testid=\'stButton\']').click()">Sign up</a></p>
                <p><a href="#">Forgot password?</a></p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Create Account", key="create_account_btn"):
                st.session_state.auth_page = 'signup'
                st.rerun()

def signup_page():
    st.markdown("<div class='header-title'>🚀 Create Your Account</div>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/4400/4400621.png", width=150)
        with col2:
            st.header("Create a New Account")
            with st.form("signup_form"):
                email = st.text_input("Work Email", placeholder="your@company.com")
                password = st.text_input("Password", type="password", help="Minimum 6 characters")
                confirm_password = st.text_input("Confirm Password", type="password")
                if st.form_submit_button("Create Account", use_container_width=True):
                    if password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        if firebase_auth.create_user(email, password):
                            st.success("Account created! Please login.")
                            st.session_state.auth_page = 'login'
                            st.rerun()
                        else:
                            st.error("Account creation failed. Email may be in use.")

            if st.button("Back to Login", key="back_login_btn"):
                st.session_state.auth_page = 'login'
                st.rerun()

# --- Main app page ---

def main_app():
    st.markdown("<div class='header-title'>📄 AI Resume Screening Pro</div>", unsafe_allow_html=True)

    st.sidebar.title("Options")
    st.sidebar.markdown("### Job Description")

    jd_options = load_job_descriptions()
    jd_list = list(jd_options.keys())
    selected_jd = st.sidebar.selectbox("Select Job Title", jd_list)

    jd_text = jd_options[selected_jd]
    jd_text_edit = st.sidebar.text_area("Job Description Text", value=jd_text, height=150)

    if st.sidebar.button("Save Job Description"):
        jd_options[selected_jd] = jd_text_edit
        save_job_descriptions(jd_options)
        st.sidebar.success("Job Description saved!")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Upload Resumes")
    uploaded_files = st.sidebar.file_uploader("Upload PDF Resumes", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        if st.button("Process Resumes"):
            with st.spinner("Analyzing Resumes..."):
                st.session_state.processing = True
                st.session_state.results = process_resumes(uploaded_files, jd_text_edit)
                st.session_state.processing = False

    # Show results if available
    if st.session_state.results:
        df = pd.DataFrame(st.session_state.results).drop(columns=["Raw Text"], errors='ignore')
        df = df.sort_values(by="Match %", ascending=False).reset_index(drop=True)

        st.markdown("### Screening Results")
        st.dataframe(df.style.background_gradient(subset=["Match %"], cmap="Greens"))

        selected_candidate = st.selectbox("Select Candidate to Preview Resume Text", options=df['Candidate'])
        if selected_candidate:
            candidate_data = next((item for item in st.session_state.results if item["Candidate"] == selected_candidate), None)
            if candidate_data:
                st.markdown(f"**Resume Text Preview for {selected_candidate}**")
                with st.expander("Show full extracted text"):
                    st.text_area("Extracted Resume Text", value=candidate_data.get("Raw Text", ""), height=300)

        # Downloadable Report
        report_str = generate_report(df, selected_jd, jd_text_edit)
        st.download_button(
            label="📥 Download Screening Report (TXT)",
            data=report_str,
            file_name=f"screening_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    else:
        st.info("Upload PDF resumes and click 'Process Resumes' to start screening.")

    # Logout button
    if st.button("Logout"):
        firebase_auth.logout()
        st.session_state.auth_page = 'login'
        st.experimental_rerun()

# --- Main entry point ---

def main():
    if st.session_state.auth_page == 'login':
        login_page()
    elif st.session_state.auth_page == 'signup':
        signup_page()
    else:
        main_app()

if __name__ == "__main__":
    main()