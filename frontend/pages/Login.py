import os

import requests
import streamlit as st


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000"
)

LOGIN_URL = f"{BACKEND_URL}/auth/login"


st.set_page_config(
    page_title="Login - AI Resume Analyzer",
    layout="centered"
)


st.title("Welcome Back")

st.caption(
    "Log in to analyze resumes and access your history."
)

st.divider()


with st.form("login_form"):

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    submitted = st.form_submit_button(
        "Login",
        use_container_width=True
    )


if submitted:

    if not email or not password:

        st.error(
            "Please enter your email and password."
        )

    else:

        try:

            response = requests.post(
                LOGIN_URL,
                json={
                    "email": email,
                    "password": password
                }
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI backend."
            )

            st.stop()

        if response.status_code != 200:

            try:
                detail = response.json().get(
                    "detail",
                    "Login failed."
                )
            except Exception:
                detail = "Login failed."

            st.error(detail)

        else:

            data = response.json()

            st.session_state["access_token"] = (
                data["access_token"]
            )

            st.session_state["user_email"] = email

            st.success(
                "Login successful!"
            )

            st.switch_page("Home.py")


st.divider()

st.caption(
    "Don't have an account?"
)

if st.button(
    "Create an Account",
    use_container_width=True
):

    st.switch_page(
        "pages/Register.py"
    )