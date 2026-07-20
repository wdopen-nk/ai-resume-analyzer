import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.subheader("Tech Stack")

        st.write("1. Python")
        st.write("2. FastAPI")
        st.write("3. Ollama")
        st.write("4. Streamlit")
        st.write("5. SQLite")

        st.divider()
        st.caption("Version 1.0.0")