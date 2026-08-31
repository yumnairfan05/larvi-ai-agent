import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


# =========================
# GOOGLE SCOPES
# =========================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
]


# =========================
# TOKEN PATH
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

TOKEN_PATH = os.path.join(
    BASE_DIR,
    "token.json"
)


# =========================
# LOAD GOOGLE CREDENTIALS
# =========================

def get_google_credentials():

    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(
            "token.json not found. Please connect your Google account first."
        )

    credentials = Credentials.from_authorized_user_file(
        TOKEN_PATH,
        SCOPES
    )

    return credentials


# =========================
# GMAIL SERVICE
# =========================

def get_gmail_service():

    credentials = get_google_credentials()

    return build(
        "gmail",
        "v1",
        credentials=credentials
    )


# =========================
# CALENDAR SERVICE
# =========================

def get_calendar_service():

    credentials = get_google_credentials()

    return build(
        "calendar",
        "v3",
        credentials=credentials
    )


# =========================
# DRIVE SERVICE
# =========================

def get_drive_service():

    credentials = get_google_credentials()

    return build(
        "drive",
        "v3",
        credentials=credentials
    )
