import os
from typing import Any

import requests
import streamlit as st


class APIService:

    BACKEND_URL = os.getenv(
        "BACKEND_URL",
        "http://backend:8000"
    )

    @staticmethod
    def _headers() -> dict[str, str]:

        token = st.session_state.get(
            "access_token"
        )

        if not token:
            return {}

        return {
            "Authorization": f"Bearer {token}"
        }

    @staticmethod
    def _handle_response(
        response: requests.Response
    ):

        if response.status_code == 401:

            st.session_state.clear()

            st.error(
                "Your session has expired. "
                "Please log in again."
            )

            st.stop()

        return response

    @classmethod
    def get(
        cls,
        endpoint: str,
        **kwargs: Any
    ) -> requests.Response:

        response = requests.get(
            f"{cls.BACKEND_URL}{endpoint}",
            headers=cls._headers(),
            **kwargs
        )

        return cls._handle_response(response)

    @classmethod
    def post(
        cls,
        endpoint: str,
        **kwargs: Any
    ) -> requests.Response:

        response = requests.post(
            f"{cls.BACKEND_URL}{endpoint}",
            headers=cls._headers(),
            **kwargs
        )

        return cls._handle_response(response)

    @classmethod
    def delete(
        cls,
        endpoint: str,
        **kwargs: Any
    ) -> requests.Response:

        response = requests.delete(
            f"{cls.BACKEND_URL}{endpoint}",
            headers=cls._headers(),
            **kwargs
        )

        return cls._handle_response(response)