from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from workflows.larvi_graph import run_larvi_workflow
from google_auth import create_google_flow


# =========================
# FASTAPI APP
# =========================

app = FastAPI(title="LARVI AI Agent")


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# CHAT MODELS
# =========================

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    category: str
    response: str


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "message": "LARVI AI Agent backend is running"
    }


# =========================
# CHAT
# =========================

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = run_larvi_workflow(
        request.message
    )

    return result


# =========================
# GOOGLE OAUTH LOGIN
# =========================

@app.get("/auth/google")
def google_login():

    flow = create_google_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    return RedirectResponse(
        authorization_url
    )


# =========================
# GOOGLE OAUTH CALLBACK
# =========================

@app.get("/auth/google/callback")
def google_callback(code: str):

    flow = create_google_flow()

    flow.fetch_token(
        code=code
    )

    credentials = flow.credentials

    token_data = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    import json

    with open(
        "token.json",
        "w"
    ) as token_file:

        json.dump(
            token_data,
            token_file,
            indent=2
        )

    return {
        "message": "Google account connected successfully!",
        "scopes": credentials.scopes,
    }