import os

import requests
import streamlit as st

from components.sidebar import render_sidebar


# ============================================================
# Configuration
# ============================================================

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000"
)

HISTORY_API_URL = f"{BACKEND_URL}/resume/history"
MATCH_API_URL = f"{BACKEND_URL}/resume/match"


st.set_page_config(
    page_title="Job Matcher",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# Sidebar
# ============================================================

render_sidebar()


# ============================================================
# Helper Functions
# ============================================================

def get_match_label(score):
    """Return a human-readable label for a match score."""

    if score >= 80:
        return "Excellent Match"

    if score >= 60:
        return "Good Match"

    if score >= 40:
        return "Moderate Match"

    return "Weak Match"


def render_list(items, empty_message):
    """Render a list using native Streamlit components."""

    if not items:
        st.caption(empty_message)
        return

    for item in items:
        st.markdown(f"- {item}")


# ============================================================
# Page Header
# ============================================================

st.title("Job Matcher")

st.caption(
    "Compare your resume against a specific job description "
    "and identify your strengths, gaps, and improvement areas."
)

st.divider()


# ============================================================
# Load Resume History
# ============================================================

try:

    response = requests.get(
        HISTORY_API_URL,
        timeout=10
    )

except requests.exceptions.ConnectionError:

    st.error(
        "Cannot connect to the FastAPI backend."
    )

    st.stop()

except requests.exceptions.Timeout:

    st.error(
        "The request to the backend timed out."
    )

    st.stop()

except requests.exceptions.RequestException:

    st.error(
        "An error occurred while loading your resumes."
    )

    st.stop()


if response.status_code != 200:

    st.error(
        "Unable to load your analyzed resumes."
    )

    st.stop()


try:

    history = response.json()

except ValueError:

    st.error(
        "The backend returned an invalid response."
    )

    st.stop()


# ============================================================
# No Resume Available
# ============================================================

if not history:

    st.info(
        """
        No analyzed resumes yet.

        Upload and analyze a resume from the **Home** page
        before using the Job Matcher.
        """
    )

    st.stop()


# ============================================================
# Resume Selection
# ============================================================

st.subheader("1. Select Your Resume")

resume_options = {}

for item in history:

    label = (
        f'{item["filename"]} '
        f'• Score: {item["resume_score"]}/100'
    )

    resume_options[label] = item["id"]


selected_resume_label = st.selectbox(
    "Resume",
    options=list(resume_options.keys()),
    label_visibility="collapsed"
)

selected_resume_id = resume_options[
    selected_resume_label
]


# ============================================================
# Job Information
# ============================================================

st.subheader("2. Enter Job Information")

job_title = st.text_input(
    "Job Title",
    placeholder="e.g. Backend Developer"
)

job_description = st.text_area(
    "Job Description",
    placeholder=(
        "Paste the complete job description here..."
    ),
    height=260
)

st.caption(
    "For the best results, include the complete job description, "
    "especially required skills, technologies, responsibilities, "
    "and qualifications."
)


# ============================================================
# Analyze Button
# ============================================================

st.write("")

analyze_button = st.button(
    "Analyze Job Match",
    type="primary",
    use_container_width=True
)


# ============================================================
# Run Job Match
# ============================================================

if analyze_button:

    if not job_title.strip():

        st.warning(
            "Please enter a job title."
        )

        st.stop()


    if len(job_description.strip()) < 20:

        st.warning(
            "Please enter a job description "
            "containing at least 20 characters."
        )

        st.stop()


    payload = {
        "resume_id": selected_resume_id,
        "job_title": job_title.strip(),
        "job_description": job_description.strip()
    }


    with st.spinner(
        "AI is comparing your resume with the job..."
    ):

        try:

            response = requests.post(
                MATCH_API_URL,
                json=payload,
                timeout=180
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to the FastAPI backend."
            )

            st.stop()

        except requests.exceptions.Timeout:

            st.error(
                "The AI analysis took too long. "
                "Please try again."
            )

            st.stop()

        except requests.exceptions.RequestException:

            st.error(
                "An error occurred while contacting "
                "the backend."
            )

            st.stop()


    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Unable to analyze the job match."
            )

        except Exception:

            detail = (
                "Unable to analyze the job match."
            )

        st.error(detail)

        st.stop()


    try:

        result = response.json()

    except ValueError:

        st.error(
            "The backend returned an invalid match result."
        )

        st.stop()


    # Save result across Streamlit reruns.
    st.session_state["job_match_result"] = result


# ============================================================
# Retrieve Existing Result
# ============================================================

result = st.session_state.get(
    "job_match_result"
)


if result is None:

    st.divider()

    st.info(
        """
        Enter a job title and job description above,
        then click **Analyze Job Match** to see the results.
        """
    )

    st.stop()


# ============================================================
# Results
# ============================================================

st.divider()

job_title_result = result.get(
    "job_title",
    job_title
)

st.header(
    f"Match Results"
)

st.caption(
    job_title_result
)


# ============================================================
# Overall Match
# ============================================================

match_score = result.get(
    "match_score",
    0
)

match_label = get_match_label(
    match_score
)


st.subheader("Overall Match")


with st.container(border=True):

    score_col, description_col = st.columns(
        [1, 2]
    )

    with score_col:

        st.metric(
            "Match Score",
            f"{match_score}/100"
        )

    with description_col:

        if match_score >= 80:

            st.success(
                f"### {match_label}\n"
                "Your resume aligns very well with this position."
            )

        elif match_score >= 60:

            st.info(
                f"### {match_label}\n"
                "Your resume has a solid alignment with this position."
            )

        elif match_score >= 40:

            st.warning(
                f"### {match_label}\n"
                "There are several areas where your resume could be improved."
            )

        else:

            st.error(
                f"### {match_label}\n"
                "Your resume currently has significant gaps for this position."
            )

    st.progress(
        min(max(match_score, 0), 100) / 100
    )


# ============================================================
# Score Breakdown
# ============================================================

st.subheader("Score Breakdown")


skills_match = result.get(
    "skills_match",
    0
)

experience_match = result.get(
    "experience_match",
    0
)

keyword_match = result.get(
    "keyword_match",
    0
)


col1, col2, col3 = st.columns(3)


with col1:

    with st.container(border=True):

        st.metric(
            "Skills Match",
            f"{skills_match}%"
        )

        st.progress(
            min(max(skills_match, 0), 100) / 100
        )


with col2:

    with st.container(border=True):

        st.metric(
            "Experience Match",
            f"{experience_match}%"
        )

        st.progress(
            min(max(experience_match, 0), 100) / 100
        )


with col3:

    with st.container(border=True):

        st.metric(
            "Keyword Match",
            f"{keyword_match}%"
        )

        st.progress(
            min(max(keyword_match, 0), 100) / 100
        )


st.divider()


# ============================================================
# Skills Analysis
# ============================================================

st.subheader("Skills Analysis")


matching_skills = result.get(
    "matching_skills",
    []
)

missing_skills = result.get(
    "missing_skills",
    []
)


col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.markdown("### Matching Skills")

        if matching_skills:

            render_list(
                matching_skills,
                "No matching skills identified."
            )

        else:

            st.caption(
                "No matching skills identified."
            )


with col2:

    with st.container(border=True):

        st.markdown("### Missing Skills")

        if missing_skills:

            render_list(
                missing_skills,
                "No important missing skills identified."
            )

        else:

            st.caption(
                "No important missing skills identified."
            )


st.write("")


# ============================================================
# Keyword Analysis
# ============================================================

st.subheader("Keyword Analysis")


matching_keywords = result.get(
    "matching_keywords",
    []
)

missing_keywords = result.get(
    "missing_keywords",
    []
)


col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.markdown("### Matching Keywords")

        render_list(
            matching_keywords,
            "No matching keywords identified."
        )


with col2:

    with st.container(border=True):

        st.markdown("### Missing Keywords")

        render_list(
            missing_keywords,
            "No important missing keywords identified."
        )


st.divider()


# ============================================================
# Recommendations
# ============================================================

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

        with st.container(border=True):

            st.markdown(
                f"**{index}.** {recommendation}"
            )

        st.write("")

else:

    st.info(
        "No additional recommendations were generated."
    )


# ============================================================
# Start New Match
# ============================================================

st.divider()

if st.button(
    "Start New Job Match",
    use_container_width=True
):

    st.session_state.pop(
        "job_match_result",
        None
    )

    st.rerun()