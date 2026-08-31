import os

from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow


# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


# =========================
# GOOGLE OAUTH SETTINGS
# =========================

REDIRECT_URI = "http://127.0.0.1:8000/auth/google/callback"


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
]


# =========================
# CREATE GOOGLE OAUTH FLOW
# =========================

def create_google_flow():

    if not GOOGLE_CLIENT_ID:
        raise ValueError(
            "GOOGLE_CLIENT_ID is missing from .env"
        )

    if not GOOGLE_CLIENT_SECRET:
        raise ValueError(
            "GOOGLE_CLIENT_SECRET is missing from .env"
        )

    client_config = {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                REDIRECT_URI
            ],
        }
    }

    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    return flow
