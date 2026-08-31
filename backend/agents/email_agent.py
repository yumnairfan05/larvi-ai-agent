from tools.gmail_tools import (
    get_unread_emails,
    get_recent_emails,
    search_emails,
    read_email,
    delete_email,
    send_email,
)

from agent import call_ollama


# =========================================================
# FORMAT EMAIL LIST
# =========================================================

def format_email_list(
    emails,
    heading="Emails"
):

    if not emails:
        return "No matching emails found."

    response = f"{heading}:\n\n"

    for index, email in enumerate(
        emails,
        start=1
    ):

        response += (
            f"{index}. "
            f"From: {email.get('from', '')}\n"
            f"Subject: {email.get('subject', '')}\n"
            f"Date: {email.get('date', '')}\n"
            f"ID: {email.get('id', '')}\n\n"
        )

    return response


# =========================================================
# READ UNREAD EMAILS
# =========================================================

def handle_read_emails():

    emails = get_unread_emails(
        max_results=10
    )

    if not emails:

        return (
            "You don't have any unread emails."
        )

    return format_email_list(
        emails,
        heading="Here are your unread emails"
    )


# =========================================================
# READ RECENT EMAILS
# =========================================================

def handle_recent_emails():

    emails = get_recent_emails(
        max_results=10
    )

    if not emails:

        return "You don't have any recent emails."

    return format_email_list(
        emails,
        heading="Here are your latest emails"
    )


# =========================================================
# OPEN / READ ONE EMAIL
# =========================================================

def handle_read_email(
    message_id: str
):

    if not message_id:

        return (
            "I couldn't determine which email "
            "you want me to read."
        )

    email = read_email(
        message_id
    )

    if not email.get("success"):

        return (
            "I couldn't open that email.\n"
            f"Error: {email.get('error', 'Unknown error')}"
        )

    body = email.get(
        "body",
        ""
    )

    if not body:
        body = "(No readable email body found.)"

    return (
        f"From: {email.get('from', '')}\n"
        f"To: {email.get('to', '')}\n"
        f"Subject: {email.get('subject', '')}\n"
        f"Date: {email.get('date', '')}\n\n"
        f"Email:\n"
        f"{body}"
    )


# =========================================================
# SUMMARIZE EMAIL
# =========================================================

def handle_summarize_email(
    message_id: str
):

    if not message_id:

        return (
            "I couldn't determine which email "
            "you want me to summarize."
        )

    email = read_email(
        message_id
    )

    if not email.get("success"):

        return (
            "I couldn't open the email for "
            "summarization."
        )

    body = email.get(
        "body",
        ""
    )

    if not body:

        return (
            "The email does not contain a "
            "readable message body."
        )

    prompt = f"""
You are LARVI's email summarization assistant.

Summarize the following email clearly.

Include:

1. Main topic
2. Important points
3. Important dates or times
4. Required actions
5. Important people mentioned

If the email contains a meeting or appointment,
clearly mention:

- Meeting title
- Date
- Time
- Location
- People involved

Do not invent information.

EMAIL:

From: {email.get('from', '')}

Subject: {email.get('subject', '')}

Date: {email.get('date', '')}

Body:

{body}
"""

    try:

        summary = call_ollama([
            {
                "role": "system",
                "content": (
                    "You summarize emails accurately. "
                    "Never invent information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ])

        return (
            f"Email Summary:\n\n"
            f"From: {email.get('from', '')}\n"
            f"Subject: {email.get('subject', '')}\n\n"
            f"{summary}"
        )

    except Exception as e:

        return (
            "I couldn't summarize the email.\n"
            f"Error: {str(e)}"
        )


# =========================================================
# SEARCH EMAILS
# =========================================================

def handle_search_emails(
    query: str
):

    if not query:

        return (
            "Please tell me what emails "
            "you want me to search for."
        )

    emails = search_emails(
        query=query,
        max_results=10
    )

    return format_email_list(
        emails,
        heading="Here are the matching emails"
    )


# =========================================================
# DELETE EMAIL
# =========================================================

def handle_delete_email(
    query: str
):

    if not query:

        return (
            "Please tell me which email "
            "you want me to delete."
        )

    emails = search_emails(
        query=query,
        max_results=10
    )

    if not emails:

        return (
            "I couldn't find any matching "
            "emails to delete."
        )

    if len(emails) > 1:

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
                f"Date: {email.get('date', '')}\n"
                f"ID: {email.get('id', '')}\n\n"
            )

        return response

    message_id = emails[0].get(
        "id",
        ""
    )

    result = delete_email(
        message_id
    )

    if result.get("success"):

        return (
            "Email moved to trash successfully."
        )

    return (
        "I couldn't delete the email."
    )


# =========================================================
# SEND EMAIL
# =========================================================

def handle_send_email(
    to: str,
    subject: str,
    body: str
):

    result = send_email(
        to=to,
        subject=subject,
        body=body
    )

    if result.get("success"):

        return (
            "Email sent successfully."
        )

    return (
        "I couldn't send the email.\n"
        f"Error: {result.get('error', '')}"
    )


# =========================================================
# EMAIL AGENT
# =========================================================

def email_agent(
    action: str,
    to: str = "",
    subject: str = "",
    body: str = "",
    query: str = "",
    message_id: str = ""
):

    action = action.lower().strip()

    # =====================================================
    # READ UNREAD
    # =====================================================

    if action == "read":

        return handle_read_emails()

    # =====================================================
    # RECENT EMAILS
    # =====================================================

    if action == "recent":

        return handle_recent_emails()

    # =====================================================
    # OPEN EMAIL
    # =====================================================

    if action == "open":

        return handle_read_email(
            message_id
        )

    # =====================================================
    # SUMMARIZE EMAIL
    # =====================================================

    if action == "summarize":

        return handle_summarize_email(
            message_id
        )

    # =====================================================
    # SEARCH
    # =====================================================

    if action == "search":

        return handle_search_emails(
            query
        )

    # =====================================================
    # DELETE
    # =====================================================

    if action == "delete":

        return handle_delete_email(
            query
        )

    # =====================================================
    # SEND
    # =====================================================

    if action == "send":

        if not to:

            return (
                "Please provide the recipient's "
                "email address."
            )

        if not subject:

            return (
                "Please provide an email subject."
            )

        if not body:

            return (
                "Please provide the email body."
            )

        return handle_send_email(
            to=to,
            subject=subject,
            body=body
        )

    return (
        "I don't recognize that email action."
    )
