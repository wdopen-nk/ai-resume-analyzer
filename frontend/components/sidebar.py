import streamlit as st

from components.auth import is_authenticated, logout


def render_sidebar():

    with st.sidebar:

        st.caption("Tech Stack")
        
        st.write("Python")
        st.write("FastAPI")
        st.write("Ollama")
        st.write("Streamlit")
        st.write("SQLite")
        
        st.divider()

        if is_authenticated():

            user_email = st.session_state.get(
                "user_email",
                "User"
            )

            st.caption(
                f"Logged in as: {user_email}"
            )

            if st.button(
                "Logout",
                use_container_width=True
            ):
                logout()

        st.caption("Version 1.0.0")