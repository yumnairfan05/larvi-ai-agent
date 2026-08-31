# =========================================================
# LARVI CONFIGURATION
# =========================================================

import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# APPLICATION
# =========================================================

APP_NAME = "LARVI AI Agent"

APP_VERSION = "1.0.0"


# =========================================================
# TIMEZONE
# =========================================================

TIMEZONE_NAME = "Asia/Karachi"

PAKISTAN_TZ = ZoneInfo(
    TIMEZONE_NAME
)


# =========================================================
# OLLAMA
# =========================================================

OLLAMA_API_KEY = os.getenv(
    "OLLAMA_API_KEY"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "gpt-oss:20b"
)

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "https://ollama.com/api/chat"
)


# =========================================================
# GOOGLE
# =========================================================

GOOGLE_CLIENT_SECRET_FILE = os.getenv(
    "GOOGLE_CLIENT_SECRET_FILE",
    "credentials.json"
)

GOOGLE_TOKEN_FILE = os.getenv(
    "GOOGLE_TOKEN_FILE",
    "token.json"
)


# =========================================================
# GOOGLE SCOPES
# =========================================================

GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
]


# =========================================================
# GOOGLE CALENDAR
# =========================================================

GOOGLE_CALENDAR_ID = os.getenv(
    "GOOGLE_CALENDAR_ID",
    "primary"
)


# =========================================================
# GMAIL
# =========================================================

GMAIL_USER_ID = os.getenv(
    "GMAIL_USER_ID",
    "me"
)


# =========================================================
# API CONFIGURATION
# =========================================================

BACKEND_HOST = os.getenv(
    "BACKEND_HOST",
    "127.0.0.1"
)

BACKEND_PORT = int(
    os.getenv(
        "BACKEND_PORT",
        "8000"
    )
)


# =========================================================
# FRONTEND
# =========================================================

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)


# =========================================================
# CORS
# =========================================================

CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",

    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
]


# =========================================================
# LARVI SETTINGS
# =========================================================

MAX_EMAIL_RESULTS = int(
    os.getenv(
        "MAX_EMAIL_RESULTS",
        "10"
    )
)

MAX_CALENDAR_RESULTS = int(
    os.getenv(
        "MAX_CALENDAR_RESULTS",
        "10"
    )
)

MAX_DRIVE_RESULTS = int(
    os.getenv(
        "MAX_DRIVE_RESULTS",
        "10"
    )
)


# =========================================================
# VALID REQUEST CATEGORIES
# =========================================================

VALID_CATEGORIES = {
    "GENERAL",
    "EMAIL",
    "CALENDAR",
    "DRIVE",
}


# =========================================================
# VALID EMAIL ACTIONS
# =========================================================

VALID_EMAIL_ACTIONS = {
    "read",
    "recent",
    "search",
    "open",
    "summarize",
    "send",
    "delete",
}


# =========================================================
# VALID CALENDAR ACTIONS
# =========================================================

VALID_CALENDAR_ACTIONS = {
    "view",
    "find",
    "create",
    "update",
    "delete",
}


# =========================================================
# HELPER: CHECK OLLAMA CONFIGURATION
# =========================================================

def validate_config():

    if not OLLAMA_API_KEY:

        raise RuntimeError(
            "OLLAMA_API_KEY is missing from "
            "the environment variables."
        )


# =========================================================
# CONFIG SUMMARY
# =========================================================

def get_config():

    return {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "timezone": TIMEZONE_NAME,

        "ollama_model": OLLAMA_MODEL,

        "google_client_secret_file":
            GOOGLE_CLIENT_SECRET_FILE,

        "google_token_file":
            GOOGLE_TOKEN_FILE,

        "google_calendar_id":
            GOOGLE_CALENDAR_ID,

        "gmail_user_id":
            GMAIL_USER_ID,

        "backend_host":
            BACKEND_HOST,

        "backend_port":
            BACKEND_PORT,

        "frontend_url":
            FRONTEND_URL,
    }
