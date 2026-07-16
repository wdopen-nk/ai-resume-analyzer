import streamlit as st

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")

st.write(
    """
Welcome!

Upload your resume and receive AI-powered feedback.

Features:

- Resume Score
- ATS Score
- Strengths
- Weaknesses
- Missing Skills
- Recommendations
"""
)

st.info("Resume analysis will be available in Sprint 2.")