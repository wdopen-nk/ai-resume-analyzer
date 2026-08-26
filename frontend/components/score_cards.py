import streamlit as st


def _score_label(score):
    if score >= 80:
        return "Excellent"

    if score >= 60:
        return "Good"

    if score >= 40:
        return "Fair"

    return "Needs Improvement"


def render_scores(
    resume_score,
    ats_score,
    skills_score=0,
):

    st.subheader("Overall Scores")

    scores = [
        ("Resume Score", resume_score),
        ("ATS Score", ats_score),
        ("Skills Score", skills_score),
    ]

    col1, col2, col3 = st.columns(3)

    for column, (label, score) in zip(
        [col1, col2, col3],
        scores
    ):

        with column:

            st.metric(
                label,
                f"{score}/100",
                help=_score_label(score)
            )

            st.progress(
                min(max(score, 0), 100) / 100
            )

            st.caption(
                _score_label(score)
            )

    st.divider()