import json
from datetime import datetime
from zoneinfo import ZoneInfo

from agent import classify_request, call_ollama
from agents.email_agent import email_agent
from agents.calendar_agent import calendar_agent


# =========================================================
# TIMEZONE
# =========================================================

PAKISTAN_TZ = ZoneInfo("Asia/Karachi")


def get_current_datetime():

    now = datetime.now(PAKISTAN_TZ)

    return now.strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )


# =========================================================
# JSON PARSER
# =========================================================

def parse_json_response(result: str):

    result = result.strip()

    if result.startswith("```"):

        result = result.replace(
            "```json",
            ""
        )

        result = result.replace(
            "```",
            ""
        )

        result = result.strip()

    return json.loads(result)


# =========================================================
# EMAIL COMMAND PARSER
# =========================================================

def parse_email_command(message: str):

    prompt = f"""
You are LARVI's email command parser.

Your job is to understand the user's email request
and convert it into JSON.

Return ONLY valid JSON.

JSON FORMAT:

{{
    "action": "",
    "to": "",
    "subject": "",
    "body": "",
    "query": "",
    "message_id": ""
}}

Allowed actions:

read
recent
search
open
summarize
send
delete


=========================================================
READ UNREAD EMAILS
=========================================================

Use "read" when the user wants unread emails.

Examples:

"Show my unread emails"

"Read my unread emails"


=========================================================
RECENT EMAILS
=========================================================

Use "recent" when the user wants their latest emails.

Examples:

"Show my latest emails"

"Show my recent emails"

"What emails did I receive recently?"


=========================================================
SEARCH EMAILS
=========================================================

Use "search" when the user wants to find specific emails.

Examples:

"Find emails from Ahmed"

query:

from:Ahmed


"Find emails about the project"

query:

project


"Find emails with subject meeting"

query:

subject:meeting


=========================================================
OPEN / READ A SPECIFIC EMAIL
=========================================================

Use "open" when the user wants to read the actual
contents of a specific email.

Examples:

"Open the email from Ahmed"

"Read the email about the project"

"Read the email from Sarah about the meeting"

For these requests, create a Gmail search query
in "query".

Examples:

from:Ahmed

project

from:Sarah meeting


IMPORTANT:

Do NOT invent a message_id.

Leave message_id empty.

The system will search for the email first.


=========================================================
SUMMARIZE EMAIL
=========================================================

Use "summarize" when the user wants a summary of
an email.

Examples:

"Summarize my latest email"

"Summarize the email from Ahmed"

"Give me a summary of the project email"

For a specific email, put a Gmail search query
in "query".

Examples:

from:Ahmed

project

subject:meeting


=========================================================
SEND EMAIL
=========================================================

Use "send" when the user wants to send an email.

Never invent an email address.

If recipient is missing:

"to": ""

If subject is missing, create a short appropriate
subject.

If body is missing:

"body": ""


=========================================================
DELETE EMAIL
=========================================================

Use "delete" only when the user explicitly wants
to delete, remove, or trash an email.

Examples:

"Delete the email from Ahmed"

"Remove the project email"

"Trash the email with subject meeting"

Put the Gmail query in "query".


=========================================================
IMPORTANT RULES
=========================================================

1. Return ONLY JSON.

2. Never return markdown.

3. Never invent a message ID.

4. Never invent an email address.

5. Use empty strings for unknown fields.

6. Use Gmail search syntax in "query".

7. For open/summarize requests, use "query"
   so LARVI can find the email.

8. For send, use "to", "subject", and "body".

9. Delete only when explicitly requested.

10. Do not confuse calendar requests with email requests.


USER REQUEST:

{message}
"""

    result = call_ollama([
        {
            "role": "system",
            "content": (
                "You extract email commands "
                "into valid JSON only."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ])

    return parse_json_response(result)


# =========================================================
# FIND EMAIL FOR OPEN / SUMMARIZE
# =========================================================

def find_email_for_action(query: str):

    from tools.gmail_tools import search_emails

    if not query:

        return {
            "success": False,
            "response": (
                "Please tell me which email "
                "you mean."
            )
        }

    emails = search_emails(
        query=query,
        max_results=10
    )

    if not emails:

        return {
            "success": False,
            "response": (
                f"I couldn't find an email "
                f"matching '{query}'."
            )
        }

    # =====================================================
    # ONE EMAIL
    # =====================================================

    if len(emails) == 1:

        return {
            "success": True,
            "email": emails[0]
        }

    # =====================================================
    # MULTIPLE EMAILS
    # =====================================================

    response = (
        "I found multiple matching emails. "
        "Please be more specific:\n\n"
    )

    for index, email in enumerate(
        emails,
        start=1
    ):

        response += (
            f"{index}. "
            f"From: {email.get('from', '')}\n"
            f"Subject: {email.get('subject', '')}\n"
            f"Date: {email.get('date', '')}\n\n"
        )

    return {
        "success": False,
        "response": response
    }


# =========================================================
# MAIN LARVI WORKFLOW
# =========================================================

def run_larvi_workflow(message: str):

    # =====================================================
    # CLASSIFY REQUEST
    # =====================================================

    category = classify_request(
        message
    )

    # =====================================================
    # EMAIL
    # =====================================================

    if category == "EMAIL":

        try:

            data = parse_email_command(
                message
            )

        except (
            json.JSONDecodeError,
            TypeError
        ):

            return {
                "category": "EMAIL",
                "response": (
                    "I couldn't understand "
                    "the email request."
                )
            }

        action = data.get(
            "action",
            ""
        ).lower().strip()

        # =================================================
        # OPEN EMAIL
        # =================================================

        if action == "open":

            result = find_email_for_action(
                data.get(
                    "query",
                    ""
                )
            )

            if not result.get("success"):

                return {
                    "category": "EMAIL",
                    "response": result.get(
                        "response",
                        "I couldn't find the email."
                    )
                }

            email = result["email"]

            response = email_agent(
                action="open",
                message_id=email.get(
                    "id",
                    ""
                )
            )

            return {
                "category": "EMAIL",
                "response": response
            }

        # =================================================
        # SUMMARIZE EMAIL
        # =================================================

        if action == "summarize":

            # ---------------------------------------------
            # SEARCH FOR EMAIL
            # ---------------------------------------------

            result = find_email_for_action(
                data.get(
                    "query",
                    ""
                )
            )

            if not result.get("success"):

                return {
                    "category": "EMAIL",
                    "response": result.get(
                        "response",
                        "I couldn't find the email."
                    )
                }

            email = result["email"]

            # ---------------------------------------------
            # SEND EMAIL TO AGENT
            # ---------------------------------------------

            response = email_agent(
                action="summarize",
                message_id=email.get(
                    "id",
                    ""
                )
            )

            return {
                "category": "EMAIL",
                "response": response
            }

        # =================================================
        # NORMAL EMAIL ACTIONS
        # =================================================

        response = email_agent(
            action=action,

            to=data.get(
                "to",
                ""
            ),

            subject=data.get(
                "subject",
                ""
            ),

            body=data.get(
                "body",
                ""
            ),

            query=data.get(
                "query",
                ""
            ),

            message_id=data.get(
                "message_id",
                ""
            )
        )

        return {
            "category": "EMAIL",
            "response": response
        }

    # =====================================================
    # CALENDAR
    # =====================================================

    if category == "CALENDAR":

        current_time = get_current_datetime()

        prompt = f"""
You are LARVI's calendar command parser.

Current date and time in Pakistan:

{current_time}

Timezone:

Asia/Karachi

User request:

{message}

Return ONLY valid JSON.

FORMAT:

{{
    "action": "view" or "find" or "create" or "update" or "delete",
    "search_text": "",
    "summary": "",
    "start_time": "",
    "end_time": "",
    "description": "",
    "location": "",
    "event_id": ""
}}

Rules:

1. VIEW

Use view when the user wants upcoming events.

2. FIND

Use find when locating an existing event.

3. CREATE

Use create for new events.

4. UPDATE

Use update when changing an event.

5. DELETE

Use delete when removing an event.

6. Never invent an event ID.

7. If the user refers to an event by name,
   put it in search_text.

8. Use Asia/Karachi timezone.

9. "tomorrow" means the next Pakistan calendar day.

10. "today" means today's Pakistan calendar date.

11. If a start time is given without an end time,
    use a one-hour duration.

12. For update/delete, use search_text when
    event_id is unavailable.

13. Return empty strings for unknown fields.


USER REQUEST:

{message}
"""

        result = call_ollama([
            {
                "role": "system",
                "content": (
                    "You extract calendar commands "
                    "into valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ])

        try:

            data = parse_json_response(
                result
            )

        except (
            json.JSONDecodeError,
            TypeError
        ):

            return {
                "category": "CALENDAR",
                "response": (
                    "I couldn't understand "
                    "the calendar request."
                )
            }

        action = data.get(
            "action",
            ""
        ).lower().strip()

        search_text = data.get(
            "search_text",
            ""
        )

        event_id = data.get(
            "event_id",
            ""
        )

        # =================================================
        # FIND EVENT ID
        # =================================================

        if action in [
            "update",
            "delete"
        ]:

            if not event_id:

                from tools.calendar_tools import (
                    find_calendar_events
                )

                if not search_text:

                    return {
                        "category": "CALENDAR",
                        "response": (
                            "Please tell me which "
                            "event you mean."
                        )
                    }

                matching_events = find_calendar_events(
                    search_text,
                    max_results=10
                )

                if not matching_events:

                    return {
                        "category": "CALENDAR",
                        "response": (
                            f"I couldn't find an upcoming "
                            f"event matching "
                            f"'{search_text}'."
                        )
                    }

                if len(matching_events) == 1:

                    event_id = matching_events[0].get(
                        "id",
                        ""
                    )

                else:

                    response = (
                        "I found multiple matching "
                        "events. Please be more specific:\n\n"
                    )

                    for index, event in enumerate(
                        matching_events,
                        start=1
                    ):

                        start = event.get(
                            "start",
                            {}
                        )

                        start_time = (
                            start.get("dateTime")
                            or start.get("date")
                            or ""
                        )

                        response += (
                            f"{index}. "
                            f"{event.get('summary', '')}\n"
                            f"Start: {start_time}\n\n"
                        )

                    return {
                        "category": "CALENDAR",
                        "response": response
                    }

        # =================================================
        # CALENDAR AGENT
        # =================================================

        response = calendar_agent(
            action=action,

            summary=data.get(
                "summary",
                ""
            ),

            start_time=data.get(
                "start_time",
                ""
            ),

            end_time=data.get(
                "end_time",
                ""
            ),

            description=data.get(
                "description",
                ""
            ),

            location=data.get(
                "location",
                ""
            ),

            event_id=event_id,

            search_text=search_text
        )

        return {
            "category": "CALENDAR",
            "response": response
        }

    # =====================================================
    # GENERAL
    # =====================================================

    response = call_ollama([
        {
            "role": "system",
            "content": """
You are LARVI, an intelligent personal AI assistant.

Answer the user's question clearly and helpfully.

Do not claim that you performed an external
action unless a real tool successfully performed
that action.
"""
        },
        {
            "role": "user",
            "content": message
        }
    ])

    return {
        "category": "GENERAL",
        "response": response
    }
