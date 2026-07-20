import streamlit as st


def render_analysis(analysis):

    if analysis.get("summary"):

        st.subheader("📝 Summary")

        st.info(analysis["summary"])

    tab1, tab2, tab3 = st.tabs(
        [
            "Analysis",
            "Missing Skills",
            "Recommendations",
        ]
    )

    with tab1:

        st.subheader("Strengths")

        for item in analysis.get("strengths", []):

            st.success(item)

        st.subheader("Weaknesses")

        for item in analysis.get("weaknesses", []):

            st.warning(item)

    with tab2:

        for item in analysis.get("missing_skills", []):

            st.info(item)

    with tab3:

        for item in analysis.get("recommendations", []):

            st.info(f"• {item}")