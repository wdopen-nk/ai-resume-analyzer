import os

import requests
import streamlit as st


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000"
)


def get_auth_headers():
    """Return authorization headers with JWT token."""

    token = st.session_state.get("access_token")

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}"
    }


def is_authenticated() -> bool:
    """Check whether the user is logged in."""

    return bool(
        st.session_state.get("access_token")
    )


def require_auth():
    """Redirect unauthenticated users to login page."""

    if not is_authenticated():

        st.warning(
            "Please log in to access this page."
        )

        st.switch_page("pages/Login.py")


def logout():

    st.session_state.pop(
        "access_token",
        None
    )

    st.session_state.pop(
        "user_email",
        None
    )

    st.switch_page("pages/Login.py")