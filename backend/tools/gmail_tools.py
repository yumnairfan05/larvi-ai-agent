from email.mime.text import MIMEText
import base64
import html
import re

from services.google_service import get_gmail_service


# =========================================================
# HELPER: DECODE GMAIL BODY
# =========================================================

def decode_email_body(data):
    """
    Decode Gmail's base64url encoded email body.
    """

    if not data:
        return ""

    try:
        decoded = base64.urlsafe_b64decode(
            data.encode("UTF-8")
        ).decode(
            "UTF-8",
            errors="replace"
        )

        return decoded

    except Exception:
        return ""


# =========================================================
# HELPER: REMOVE HTML
# =========================================================

def clean_html(text):
    """
    Convert HTML email content into readable text.
    """

    if not text:
        return ""

    # Remove script/style blocks
    text = re.sub(
        r"<(script|style).*?>.*?</\1>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Remove HTML tags
    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    # Decode HTML entities
    text = html.unescape(text)

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# HELPER: EXTRACT EMAIL BODY
# =========================================================

def extract_email_body(payload):
    """
    Extract readable text from Gmail message payload.

    Supports:
    - text/plain
    - text/html
    - multipart messages
    """

    if not payload:
        return ""

    mime_type = payload.get(
        "mimeType",
        ""
    )

    body = payload.get(
        "body",
        {}
    )

    data = body.get(
        "data"
    )

    # -----------------------------------------------------
    # SIMPLE TEXT EMAIL
    # -----------------------------------------------------

    if mime_type == "text/plain" and data:

        return decode_email_body(data)

    # -----------------------------------------------------
    # HTML EMAIL
    # -----------------------------------------------------

    if mime_type == "text/html" and data:

        decoded = decode_email_body(data)

        return clean_html(decoded)

    # -----------------------------------------------------
    # MULTIPART EMAIL
    # -----------------------------------------------------

    parts = payload.get(
        "parts",
        []
    )

    plain_text = ""
    html_text = ""

    for part in parts:

        part_mime = part.get(
            "mimeType",
            ""
        )

        part_body = part.get(
            "body",
            {}
        )

        part_data = part_body.get(
            "data"
        )

        # Nested multipart
        if part.get("parts"):

            nested_body = extract_email_body(
                part
            )

            if nested_body:
                plain_text += (
                    nested_body + "\n"
                )

        elif part_mime == "text/plain" and part_data:

            plain_text += (
                decode_email_body(part_data)
                + "\n"
            )

        elif part_mime == "text/html" and part_data:

            html_text += (
                clean_html(
                    decode_email_body(part_data)
                )
                + "\n"
            )

    if plain_text.strip():
        return plain_text.strip()

    if html_text.strip():
        return html_text.strip()

    return ""


# =========================================================
# HELPER: GET EMAIL HEADERS
# =========================================================

def get_email_headers(headers):

    email_data = {
        "from": "",
        "to": "",
        "subject": "",
        "date": ""
    }

    for header in headers:

        name = header.get(
            "name",
            ""
        ).lower()

        value = header.get(
            "value",
            ""
        )

        if name == "from":
            email_data["from"] = value

        elif name == "to":
            email_data["to"] = value

        elif name == "subject":
            email_data["subject"] = value

        elif name == "date":
            email_data["date"] = value

    return email_data


# =========================================================
# GET UNREAD EMAILS
# =========================================================

def get_unread_emails(max_results=10):

    try:

        service = get_gmail_service()

        results = service.users().messages().list(
            userId="me",
            q="is:unread",
            maxResults=max_results
        ).execute()

        messages = results.get(
            "messages",
            []
        )

        if not messages:
            return []

        emails = []

        for message in messages:

            msg = service.users().messages().get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "To",
                    "Subject",
                    "Date"
                ]
            ).execute()

            headers = msg.get(
                "payload",
                {}
            ).get(
                "headers",
                []
            )

            header_data = get_email_headers(
                headers
            )

            email_data = {
                "id": message["id"],
                "thread_id": message.get(
                    "threadId",
                    ""
                ),
                "from": header_data["from"],
                "to": header_data["to"],
                "subject": header_data["subject"],
                "date": header_data["date"]
            }

            emails.append(
                email_data
            )

        return emails

    except Exception as e:

        print(
            f"Gmail unread email error: {e}"
        )

        return []


# =========================================================
# GET RECENT EMAILS
# =========================================================

def get_recent_emails(max_results=10):

    try:

        service = get_gmail_service()

        results = service.users().messages().list(
            userId="me",
            maxResults=max_results
        ).execute()

        messages = results.get(
            "messages",
            []
        )

        if not messages:
            return []

        emails = []

        for message in messages:

            msg = service.users().messages().get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "To",
                    "Subject",
                    "Date"
                ]
            ).execute()

            headers = msg.get(
                "payload",
                {}
            ).get(
                "headers",
                []
            )

            header_data = get_email_headers(
                headers
            )

            email_data = {
                "id": message["id"],
                "thread_id": message.get(
                    "threadId",
                    ""
                ),
                "from": header_data["from"],
                "to": header_data["to"],
                "subject": header_data["subject"],
                "date": header_data["date"]
            }

            emails.append(
                email_data
            )

        return emails

    except Exception as e:

        print(
            f"Gmail recent email error: {e}"
        )

        return []


# =========================================================
# READ FULL EMAIL
# =========================================================

def read_email(message_id: str):

    try:

        service = get_gmail_service()

        msg = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full"
        ).execute()

        payload = msg.get(
            "payload",
            {}
        )

        headers = payload.get(
            "headers",
            []
        )

        header_data = get_email_headers(
            headers
        )

        body = extract_email_body(
            payload
        )

        return {
            "success": True,
            "id": message_id,
            "thread_id": msg.get(
                "threadId",
                ""
            ),
            "from": header_data["from"],
            "to": header_data["to"],
            "subject": header_data["subject"],
            "date": header_data["date"],
            "body": body
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# SEARCH EMAILS
# =========================================================

def search_emails(
    query: str,
    max_results=10
):

    try:

        service = get_gmail_service()

        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get(
            "messages",
            []
        )

        if not messages:
            return []

        emails = []

        for message in messages:

            msg = service.users().messages().get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "To",
                    "Subject",
                    "Date"
                ]
            ).execute()

            headers = msg.get(
                "payload",
                {}
            ).get(
                "headers",
                []
            )

            header_data = get_email_headers(
                headers
            )

            email_data = {
                "id": message["id"],
                "thread_id": message.get(
                    "threadId",
                    ""
                ),
                "from": header_data["from"],
                "to": header_data["to"],
                "subject": header_data["subject"],
                "date": header_data["date"]
            }

            emails.append(
                email_data
            )

        return emails

    except Exception as e:

        print(
            f"Gmail search error: {e}"
        )

        return []


# =========================================================
# DELETE EMAIL
# =========================================================

def delete_email(
    message_id: str
):

    try:

        service = get_gmail_service()

        service.users().messages().trash(
            userId="me",
            id=message_id
        ).execute()

        return {
            "success": True
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# SEND EMAIL
# =========================================================

def send_email(
    to,
    subject,
    body
):

    try:

        service = get_gmail_service()

        message = MIMEText(body)

        message["to"] = to
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        send_message = {
            "raw": raw_message
        }

        sent_message = service.users().messages().send(
            userId="me",
            body=send_message
        ).execute()

        return {
            "success": True,
            "message_id": sent_message["id"]
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }