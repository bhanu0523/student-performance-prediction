
import os

import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT_URL = (
    "https://eap2wc-dofbzft-xv75309.snowflakecomputing.app/predict"
)

FEATURE_NAMES = [
    "STUDYHOURS",
    "ATTENDANCE",
    "RESOURCES",
    "EXTRACURRICULAR",
    "MOTIVATION",
    "INTERNET",
    "GENDER",
    "AGE",
    "LEARNINGSTYLE",
    "ONLINECOURSES",
    "DISCUSSIONS",
    "ASSIGNMENTCOMPLETION",
    "EDUTECH",
    "STRESSLEVEL",
]


def get_snowflake_token():
    """Get the token from local .env or Streamlit Secrets."""
    token = os.getenv("SNOWFLAKE_PAT")

    if token:
        return token

    try:
        import streamlit as st
        token = st.secrets.get("SNOWFLAKE_PAT")
    except Exception:
        token = None

    if not token:
        raise ValueError(
            "SNOWFLAKE_PAT is missing. Check your local .env file."
        )

    return token


def predict_exam_score(features):
    """Send student details to Snowflake and return the predicted score."""

    missing = [
        name for name in FEATURE_NAMES
        if name not in features
    ]

    if missing:
        raise ValueError(
            f"Missing input features: {', '.join(missing)}"
        )

    values = [features[name] for name in FEATURE_NAMES]
    token = get_snowflake_token()

    payload = {
        "dataframe_split": {
            "index": [0],
            "columns": FEATURE_NAMES,
            "data": [values],
        }
    }

    headers = {
        "Authorization": f'Snowflake Token="{token}"',
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            ENDPOINT_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )
    except requests.RequestException as error:
        raise RuntimeError(
            f"Could not connect to Snowflake: {error}"
        ) from error

    if not response.ok:
        raise RuntimeError(
            f"Snowflake returned HTTP {response.status_code}: "
            f"{response.text[:1000]}"
        )

    try:
        result = response.json()
        prediction = float(
            result["data"][0][1]["output_feature_0"]
        )
    except (ValueError, KeyError, IndexError, TypeError) as error:
        raise RuntimeError(
            f"Unexpected prediction response: {response.text[:1000]}"
        ) from error

    return prediction
