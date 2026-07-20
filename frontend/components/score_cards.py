import streamlit as st


def render_scores(
    resume_score,
    ats_score,
    skills_score=0,
):

    st.subheader("📊 Overall Scores")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Resume",
            resume_score,
        )

        st.progress(resume_score / 100)

    with col2:

        st.metric(
            "ATS",
            ats_score,
        )

        st.progress(ats_score / 100)

    with col3:

        st.metric(
            "Skills",
            skills_score,
        )

        st.progress(skills_score / 100)

    st.divider()