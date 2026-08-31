import os

import requests
import streamlit as st

from components.auth import (
    get_auth_headers,
    require_auth
)
from components.sidebar import render_sidebar
from components.score_cards import render_scores
from components.analysis_sections import render_analysis


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000"
)

API_URL = f"{BACKEND_URL}/resume"


st.set_page_config(
    page_title="History",
    layout="wide"
)


require_auth()

render_sidebar()


st.title("Resume Analysis History")

st.caption(
    "Browse your previously analyzed resumes."
)

st.divider()


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
            "Unable to load resume history."
        )

        st.stop()

    history = response.json()


except requests.exceptions.ConnectionError:

    st.error(
        "Cannot connect to backend."
    )

    st.stop()


if len(history) == 0:

    st.info(
        """
No resume analyses found.

Upload your first resume from the Home page.
"""
    )

    st.stop()


left, right = st.columns([1, 2])


with left:

    st.subheader("Resumes")

    filenames = [
        f'{item["filename"]} ({item["resume_score"]}/100)'
        for item in history
    ]

    selected = st.radio(
        "",
        filenames
    )

    index = filenames.index(selected)

    selected_resume = history[index]


with right:

    detail = requests.get(
        f'{API_URL}/{selected_resume["id"]}',
        headers=get_auth_headers()
    )

    if detail.status_code != 200:

        st.error(
            "Unable to load analysis."
        )

        st.stop()

    analysis = detail.json()

    st.subheader(
        f"📄 {analysis['filename']}"
    )

    render_scores(
        analysis["resume_score"],
        analysis["ats_score"],
        analysis.get("skills_score", 0)
    )


    if st.button(
        "Delete Resume",
        type="primary",
        use_container_width=True
    ):

        response = requests.delete(
            f"{API_URL}/{selected_resume['id']}",
            headers=get_auth_headers()
        )

        if response.status_code == 200:

            st.success(
                "Resume deleted successfully!"
            )

            st.rerun()

        else:

            st.error(
                "Unable to delete resume."
            )

    render_analysis(analysis)
