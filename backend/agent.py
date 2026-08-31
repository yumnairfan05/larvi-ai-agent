import os
import requests
from dotenv import load_dotenv

load_dotenv()


# =========================================================
# OLLAMA CONFIGURATION
# =========================================================

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "gpt-oss:20b"
)

OLLAMA_URL = "https://ollama.com/api/chat"


# =========================================================
# CALL OLLAMA
# =========================================================

def call_ollama(messages):

    if not OLLAMA_API_KEY:
        raise RuntimeError(
            "OLLAMA_API_KEY is missing"
        )

    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }

    response = requests.post(
        OLLAMA_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


# =========================================================
# CLASSIFY USER REQUEST
# =========================================================

def classify_request(message: str):

    text = message.lower().strip()

    # =====================================================
    # EMAIL KEYWORDS
    # =====================================================

    email_keywords = [
        "email",
        "emails",
        "e-mail",
        "e-mails",
        "gmail",
        "inbox",
        "mailbox",
        "mail",
        "unread email",
        "unread emails",
        "email message",
        "email messages",
    ]

    # =====================================================
    # CALENDAR KEYWORDS
    # =====================================================

    calendar_keywords = [
        "calendar",
        "event",
        "events",
        "meeting",
        "meetings",
        "appointment",
        "appointments",
        "schedule",
        "scheduled",
        "reschedule",
        "reminder",
        "reminders",
    ]

    # =====================================================
    # DRIVE KEYWORDS
    # =====================================================

    drive_keywords = [
        "google drive",
        "drive",
        "drive file",
        "drive files",
        "folder in drive",
        "document in drive",
        "file in drive",
    ]

    # =====================================================
    # DETECT EMAIL
    # =====================================================

    has_email_keyword = any(
        keyword in text
        for keyword in email_keywords
    )

    # =====================================================
    # DETECT CALENDAR
    # =====================================================

    has_calendar_keyword = any(
        keyword in text
        for keyword in calendar_keywords
    )

    # =====================================================
    # DETECT DRIVE
    # =====================================================

    has_drive_keyword = any(
        keyword in text
        for keyword in drive_keywords
    )

    # =====================================================
    # MULTI-AGENT WORKFLOW
    # =====================================================
    #
    # IMPORTANT:
    #
    # If BOTH email and calendar are involved,
    # return MULTI.
    #
    # This must happen BEFORE EMAIL/CALENDAR routing.
    #
    # =====================================================

    if has_email_keyword and has_calendar_keyword:

        return "MULTI"

    # =====================================================
    # COMMON MULTI-AGENT PHRASES
    # =====================================================

    multi_phrases = [
        "add it to my calendar",
        "add it to calendar",
        "put it on my calendar",
        "put it in my calendar",
        "schedule it",
        "schedule that",
        "calendar from email",
        "email to calendar",
        "from the email",
        "from an email",
        "from my email",
        "check my email and calendar",
        "email and calendar",
        "email then calendar",
        "calendar then email",
    ]

    has_multi_phrase = any(
        phrase in text
        for phrase in multi_phrases
    )

    if has_multi_phrase:

        return "MULTI"

    # =====================================================
    # DRIVE
    # =====================================================

    if has_drive_keyword:

        return "DRIVE"

    # =====================================================
    # EMAIL
    # =====================================================

    if has_email_keyword:

        return "EMAIL"

    # =====================================================
    # COMMON EMAIL PHRASES
    # =====================================================

    email_phrases = [
        "show my inbox",
        "open my inbox",
        "check my inbox",
        "read my inbox",
        "check my mail",
        "read my mail",
        "show my mail",
        "latest mail",
        "recent mail",
        "new mail",
        "unread mail",
    ]

    if any(
        phrase in text
        for phrase in email_phrases
    ):

        return "EMAIL"

    # =====================================================
    # CALENDAR
    # =====================================================

    if has_calendar_keyword:

        return "CALENDAR"

    # =====================================================
    # COMMON CALENDAR PHRASES
    # =====================================================

    calendar_phrases = [

        "show my calendar",
        "view my calendar",
        "check my calendar",
        "open my calendar",

        "show my events",
        "view my events",
        "check my events",

        "show upcoming events",
        "view upcoming events",
        "check upcoming events",

        "show my meetings",
        "view my meetings",
        "check my meetings",

        "show my appointments",
        "view my appointments",
        "check my appointments",

        "find my meeting",
        "find my meetings",
        "find my event",
        "find my events",

        "delete my meeting",
        "delete my event",
        "delete my appointment",

        "remove my meeting",
        "remove my event",
        "remove my appointment",

        "cancel my meeting",
        "cancel my event",
        "cancel my appointment",

        "update my meeting",
        "update my event",
        "update my appointment",

        "move my meeting",
        "move my event",
        "move my appointment",
    ]

    if any(
        phrase in text
        for phrase in calendar_phrases
    ):

        return "CALENDAR"

    # =====================================================
    # LLM CLASSIFICATION
    # =====================================================

    prompt = f"""
Classify the user's request into exactly ONE category.

Available categories:

GENERAL
CALENDAR
EMAIL
DRIVE
MULTI


=========================================================
MULTI
=========================================================

Use MULTI when the request requires BOTH:

- Email/Gmail operations
AND
- Calendar operations

The request may require multiple steps.

Examples:

"Find the email from Ali about tomorrow's meeting
and add it to my calendar"
→ MULTI

"Check whether I received an email from Ali about
tomorrow's project meeting. If you find the meeting
time, check whether I am free and add it to my calendar."
→ MULTI

"Find Ahmed's email about the project meeting and
schedule that meeting on my calendar"
→ MULTI

"Find my Project Meeting tomorrow and email Ahmed
that I will attend"
→ MULTI

"Read the meeting email and put the meeting
on my calendar"
→ MULTI

IMPORTANT:

If BOTH Gmail/email AND Calendar/event/meeting
operations are required, ALWAYS return MULTI.


=========================================================
CALENDAR
=========================================================

Use CALENDAR when the user only wants calendar
operations.

Examples:

"Create a meeting tomorrow at 5 PM"
→ CALENDAR

"Schedule a meeting with John"
→ CALENDAR

"Show my upcoming events"
→ CALENDAR

"Find my Team Meeting"
→ CALENDAR

"Update my Team Meeting"
→ CALENDAR

"Move my meeting to Friday"
→ CALENDAR

"Delete my LARVI Final Test"
→ CALENDAR


=========================================================
EMAIL
=========================================================

Use EMAIL when the user only wants email/Gmail
operations.

Examples:

"Show my emails"
→ EMAIL

"Show my latest emails"
→ EMAIL

"Show my unread emails"
→ EMAIL

"Read my emails"
→ EMAIL

"Check my inbox"
→ EMAIL

"Find emails from Sarah"
→ EMAIL

"Send an email to John"
→ EMAIL

"Reply to my last email"
→ EMAIL

"Delete my email from John"
→ EMAIL


=========================================================
DRIVE
=========================================================

Use DRIVE when the user wants Google Drive operations.

Examples:

"Find my project report in Drive"
→ DRIVE

"Read my LARVI document"
→ DRIVE

"Delete my project file from Drive"
→ DRIVE


=========================================================
GENERAL
=========================================================

Use GENERAL for:

- normal questions
- explanations
- casual conversation
- coding help
- programming questions
- writing help
- general knowledge
- unrelated requests


Examples:

"What is Python?"
→ GENERAL

"Explain machine learning"
→ GENERAL

"Help me fix my code"
→ GENERAL


=========================================================
FINAL RULE
=========================================================

Priority:

1. MULTI
2. DRIVE
3. EMAIL
4. CALENDAR
5. GENERAL

If a request requires both Email and Calendar,
return MULTI.

Return ONLY ONE category name.

Do not return explanations.

Do not return JSON.

Do not return punctuation.

Valid answers are only:

GENERAL
CALENDAR
EMAIL
DRIVE
MULTI


User request:

{message}
"""

    result = call_ollama([
        {
            "role": "system",
            "content": (
                "You are a strict request classification "
                "system. Return only one category name."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ])

    # =====================================================
    # CLEAN LLM RESPONSE
    # =====================================================

    category = result.strip().upper()

    category = category.replace(
        "```",
        ""
    ).strip()

    # =====================================================
    # VALID CATEGORIES
    # =====================================================

    valid_categories = {
        "GENERAL",
        "CALENDAR",
        "EMAIL",
        "DRIVE",
        "MULTI"
    }

    # =====================================================
    # VALIDATE RESULT
    # =====================================================

    if category not in valid_categories:

        return "GENERAL"

    return category


# =========================================================
# GENERATE GENERAL RESPONSE
# =========================================================

def generate_response(
    message: str,
    category: str
) -> str:

    system_prompt = f"""
You are LARVI, an intelligent personal AI agent.

The user's request has been classified as:

{category}

You should be helpful, clear, and honest.

IMPORTANT:

Google Calendar, Gmail, and Google Drive tools are
connected through LARVI's workflow when the request
requires an external action.

Never claim that you performed an external action
unless a real tool successfully performed that action.

If a tool is unavailable or fails, clearly tell the
user that the action could not be completed.

Do not pretend that an action was completed.
"""

    return call_ollama([
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": message
        }
    ])


# =========================================================
# ASK LARVI
# =========================================================

def ask_larvi(message: str):

    category = classify_request(
        message
    )

    response = generate_response(
        message,
        category
    )

    return {
        "category": category,
        "response": response
    }