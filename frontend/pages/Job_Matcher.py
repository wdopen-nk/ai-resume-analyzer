import os

import requests
import streamlit as st

from components.auth import (
    get_auth_headers,
    require_auth
)
from components.sidebar import render_sidebar


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000"
)

API_URL = f"{BACKEND_URL}/resume"


st.set_page_config(
    page_title="Job Matcher",
    layout="wide"
)


# Require authentication before accessing the page
require_auth()

# Render sidebar
render_sidebar()


st.title("Job Matcher")

st.caption(
    "Compare your resume with a job description and discover how well you match."
)

st.divider()


# --------------------------------------------------
# LOAD USER'S RESUME HISTORY
# --------------------------------------------------

try:

    response = requests.get(
        f"{API_URL}/history",
        headers=get_auth_headers()
    )

    if response.status_code == 401:

        st.error(
            "Your session has expired. Please log in again."
        )

        st.session_state.clear()

        st.switch_page(
            "pages/Login.py"
        )

    if response.status_code != 200:

        st.error(
            "Unable to load your resumes."
        )

        st.stop()

    resumes = response.json()


except requests.exceptions.ConnectionError:

    st.error(
        "Cannot connect to FastAPI backend."
    )

    st.stop()


# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

if not resumes:

    st.info(
        """
You haven't analyzed any resumes yet.

Upload and analyze a resume first before using the Job Matcher.
"""
    )

    if st.button(
        "Go to Resume Analyzer",
        use_container_width=True
    ):
        st.switch_page("Home.py")

    st.stop()


# --------------------------------------------------
# RESUME SELECTION
# --------------------------------------------------

st.subheader("1. Select Resume")


resume_options = {
    f'{resume["filename"]} - Score: {resume["resume_score"]}/100':
    resume["id"]
    for resume in resumes
}


selected_resume_name = st.selectbox(
    "Choose a resume",
    options=list(resume_options.keys())
)


selected_resume_id = resume_options[
    selected_resume_name
]


st.divider()


# --------------------------------------------------
# JOB DESCRIPTION INPUT
# --------------------------------------------------

st.subheader("2. Add Job Description")


job_title = st.text_input(
    "Job Title",
    placeholder="e.g. Junior Python Developer"
)


job_description = st.text_area(
    "Job Description",
    placeholder=(
        "Paste the complete job description here..."
    ),
    height=300
)


# --------------------------------------------------
# MATCH BUTTON
# --------------------------------------------------

if st.button(
    "Analyze Job Match",
    type="primary",
    use_container_width=True
):

    if not job_title.strip():

        st.error(
            "Please enter a job title."
        )

        st.stop()


    if not job_description.strip():

        st.error(
            "Please enter a job description."
        )

        st.stop()


    payload = {
        "resume_id": selected_resume_id,
        "job_title": job_title,
        "job_description": job_description
    }


    with st.spinner(
        "AI is comparing your resume with the job description..."
    ):

        try:

            response = requests.post(
                f"{API_URL}/match",
                json=payload,
                headers=get_auth_headers()
            )


        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI backend."
            )

            st.stop()


    # ----------------------------------------------
    # HANDLE AUTHENTICATION ERROR
    # ----------------------------------------------

    if response.status_code == 401:

        st.error(
            "Your session has expired. Please log in again."
        )

        st.session_state.clear()

        st.switch_page(
            "pages/Login.py"
        )


    # ----------------------------------------------
    # HANDLE OTHER ERRORS
    # ----------------------------------------------

    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Unable to analyze job match."
            )

        except Exception:

            detail = "Unable to analyze job match."

        st.error(detail)

        st.stop()


    # ----------------------------------------------
    # STORE RESULT
    # ----------------------------------------------

    result = response.json()

    st.session_state["job_match_result"] = result


# --------------------------------------------------
# DISPLAY CURRENT MATCH RESULT
# --------------------------------------------------

if "job_match_result" in st.session_state:

    result = st.session_state["job_match_result"]

    st.divider()

    st.header("Match Results")


    # ----------------------------------------------
    # SCORE CARDS
    # ----------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Overall Match",
            f'{result["match_score"]}%'
        )


    with col2:

        st.metric(
            "Skills Match",
            f'{result["skills_match"]}%'
        )


    with col3:

        st.metric(
            "Experience Match",
            f'{result["experience_match"]}%'
        )


    with col4:

        st.metric(
            "Keyword Match",
            f'{result["keyword_match"]}%'
        )


    st.divider()


    # ----------------------------------------------
    # SKILLS
    # ----------------------------------------------

    left, right = st.columns(2)


    with left:

        st.subheader("Matching Skills")

        matching_skills = result.get(
            "matching_skills",
            []
        )

        if matching_skills:

            for skill in matching_skills:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.info(
                "No matching skills detected."
            )


    with right:

        st.subheader("Missing Skills")

        missing_skills = result.get(
            "missing_skills",
            []
        )

        if missing_skills:

            for skill in missing_skills:

                st.warning(
                    f"• {skill}"
                )

        else:

            st.success(
                "No significant missing skills detected."
            )


    st.divider()


    # ----------------------------------------------
    # KEYWORDS
    # ----------------------------------------------

    left, right = st.columns(2)


    with left:

        st.subheader("Matching Keywords")

        matching_keywords = result.get(
            "matching_keywords",
            []
        )

        if matching_keywords:

            for keyword in matching_keywords:

                st.success(
                    f"✓ {keyword}"
                )

        else:

            st.info(
                "No matching keywords detected."
            )


    with right:

        st.subheader("Missing Keywords")

        missing_keywords = result.get(
            "missing_keywords",
            []
        )

        if missing_keywords:

            for keyword in missing_keywords:

                st.warning(
                    f"• {keyword}"
                )

        else:

            st.success(
                "No significant missing keywords detected."
            )


    st.divider()


    # ----------------------------------------------
    # RECOMMENDATIONS
    # ----------------------------------------------

    st.subheader("Recommendations")


    recommendations = result.get(
        "recommendations",
        []
    )


    if recommendations:

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            st.write(
                f"{index}. {recommendation}"
            )

    else:

        st.info(
            "No additional recommendations."
        )


# --------------------------------------------------
# PREVIOUS JOB MATCHES
# --------------------------------------------------

st.divider()

st.subheader("Previous Job Matches")


try:

    matches_response = requests.get(
        f"{API_URL}/{selected_resume_id}/matches",
        headers=get_auth_headers()
    )


    if matches_response.status_code == 401:

        st.session_state.clear()

        st.switch_page(
            "pages/Login.py"
        )


    if matches_response.status_code == 200:

        previous_matches = matches_response.json()

    else:

        previous_matches = []


except requests.exceptions.ConnectionError:

    previous_matches = []


if previous_matches:

    for match in previous_matches:

        with st.expander(
            f'{match["job_title"]} — '
            f'{match["match_score"]}% Match'
        ):

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Overall",
                    f'{match["match_score"]}%'
                )

            with col2:
                st.metric(
                    "Skills",
                    f'{match["skills_match"]}%'
                )

            with col3:
                st.metric(
                    "Experience",
                    f'{match["experience_match"]}%'
                )

            with col4:
                st.metric(
                    "Keywords",
                    f'{match["keyword_match"]}%'
                )


            st.markdown("### Matching Skills")

            for skill in match.get(
                "matching_skills",
                []
            ):
                st.success(f"✓ {skill}")


            st.markdown("### Missing Skills")

            for skill in match.get(
                "missing_skills",
                []
            ):
                st.warning(f"• {skill}")


            st.markdown("### Recommendations")

            for recommendation in match.get(
                "recommendations",
                []
            ):
                st.write(
                    f"• {recommendation}"
                )


else:

    st.caption(
        "No previous job matches for this resume."
    )