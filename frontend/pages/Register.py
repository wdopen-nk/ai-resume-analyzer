import os

import requests
import streamlit as st


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000"
)

REGISTER_URL = f"{BACKEND_URL}/auth/register"


st.set_page_config(
    page_title="Register - AI Resume Analyzer",
    layout="centered"
)


st.title("Create Account")

st.caption(
    "Create an account to save and manage your resume analyses."
)

st.divider()


with st.form("register_form"):

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    submitted = st.form_submit_button(
        "Create Account",
        use_container_width=True
    )


if submitted:

    if not email or not password:

        st.error(
            "Please fill in all fields."
        )

    elif password != confirm_password:

        st.error(
            "Passwords do not match."
        )

    else:

        try:

            response = requests.post(
                REGISTER_URL,
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

        if response.status_code not in [200, 201]:

            try:

                detail = response.json().get(
                    "detail",
                    "Registration failed."
                )

            except Exception:

                detail = "Registration failed."

            st.error(detail)

        else:

            st.success(
                "Account created successfully!"
            )

            st.info(
                "You can now log in."
            )

            if st.button(
                "Go to Login",
                use_container_width=True
            ):

                st.switch_page(
                    "pages/Login.py"
                )