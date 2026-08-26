import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.caption("Tech Stack")

        st.write("Python")
        st.write("FastAPI")
        st.write("Ollama")
        st.write("Streamlit")
        st.write("SQLite")

        st.divider()

        st.caption("Version 1.0.0")