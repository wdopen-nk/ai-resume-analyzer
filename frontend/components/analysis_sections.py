import streamlit as st


def _render_items(
    items,
    empty_message,
    icon,
):

    if not items:

        st.caption(empty_message)

        return

    for item in items:

        st.markdown(
            f"""
            <div style="
                padding: 12px 16px;
                margin-bottom: 8px;
                border-radius: 10px;
                border: 1px solid rgba(128,128,128,0.2);
                background: rgba(128,128,128,0.04);
            ">
                <span style="
                    font-size: 16px;
                    margin-right: 8px;
                ">
                    {icon}
                </span>
                {item}
            </div>
            """,
            unsafe_allow_html=True
        )


def render_analysis(analysis):

    if analysis.get("summary"):

        st.subheader("📝 Summary")

        st.markdown(
            f"""
            <div style="
                padding: 18px;
                border-radius: 12px;
                border: 1px solid rgba(128,128,128,0.2);
                background: rgba(128,128,128,0.04);
                line-height: 1.6;
            ">
                {analysis["summary"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")


    tab1, tab2, tab3 = st.tabs(
        [
            "Analysis",
            "Missing Skills",
            "Recommendations",
        ]
    )


    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Strengths")

            _render_items(
                analysis.get("strengths", []),
                "No strengths identified.",
                "✓",
            )

        with col2:

            st.subheader("Weaknesses")

            _render_items(
                analysis.get("weaknesses", []),
                "No weaknesses identified.",
                "!",
            )


    with tab2:

        _render_items(
            analysis.get("missing_skills", []),
            "No missing skills identified.",
            "•",
        )


    with tab3:

        _render_items(
            analysis.get("recommendations", []),
            "No recommendations available.",
            "→",
        )