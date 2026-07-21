import requests
import streamlit as st

from components.sidebar import render_sidebar
from components.page_header import render_header
from components.score_cards import render_scores
from components.analysis_sections import render_analysis

import os

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000"
)

API_URL = f"{BACKEND_URL}/resume/upload"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

render_sidebar()

render_header()

uploaded_file = st.file_uploader(
    "📤 Upload Resume",
    type=["pdf", "docx"]
)

if uploaded_file is not None:

    st.success(f"Selected file: **{uploaded_file.name}**")

    if st.button(
        "🚀 Analyze Resume",
        use_container_width=True
    ):

        with st.spinner("AI is analyzing your resume..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:

                response = requests.post(
                    API_URL,
                    files=files
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI backend."
                )

                st.stop()

            if response.status_code != 200:

                st.error(response.json()["detail"])

                st.stop()

            result = response.json()

            analysis = result["analysis"]

        st.success("✅ Analysis Completed")

        render_scores(
            analysis.get("resume_score", 0),
            analysis.get("ats_score", 0),
            analysis.get("skills_score", 0)
        )

        render_analysis(analysis)