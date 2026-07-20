import streamlit as st


def render_header():
    st.title("AI Resume Analyzer")

    st.write(
        """
Analyze your resume locally using **Ollama**.

Upload a PDF or DOCX file and receive:

- Resume Score
- ATS Score
- Strengths
- Weaknesses
- Missing Skills
- Recommendations
"""
    )

    st.divider()