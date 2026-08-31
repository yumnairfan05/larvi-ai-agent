# =========================================================
# LARVI MASTER AGENT
# =========================================================
#
# The Master Agent is responsible for:
#
# 1. Receiving the user's natural-language request
# 2. Classifying the request
# 3. Routing it to the correct agent/workflow
#
# Supported categories:
#
# GENERAL
# EMAIL
# CALENDAR
# DRIVE
#
# =========================================================

from agent import (
    classify_request,
    call_ollama,
)

from agents.email_agent import email_agent
from agents.calendar_agent import calendar_agent

# Drive agent will be added when Drive functionality
# is connected.
#
# from agents.drive_agent import drive_agent


# =========================================================
# MASTER AGENT
# =========================================================

def master_agent(message: str):
    """
    Main entry point for LARVI.

    Receives a natural-language user request,
    determines the appropriate category, and
    routes the request to the correct agent.
    """

    if not message or not message.strip():

        return {
            "category": "GENERAL",
            "response": (
                "Please tell me what you would like "
                "me to do."
            )
        }

    message = message.strip()

    # =====================================================
    # CLASSIFY REQUEST
    # =====================================================

    try:

        category = classify_request(
            message
        )

    except Exception as e:

        print(
            f"Master Agent classification error: {e}"
        )

        return {
            "category": "GENERAL",
            "response": (
                "I couldn't understand your request "
                "right now."
            )
        }

    # =====================================================
    # EMAIL
    # =====================================================

    if category == "EMAIL":

        return handle_email_request(
            message
        )

    # =====================================================
    # CALENDAR
    # =====================================================

    if category == "CALENDAR":

        return handle_calendar_request(
            message
        )

    # =====================================================
    # DRIVE
    # =====================================================

    if category == "DRIVE":

        return handle_drive_request(
            message
        )

    # =====================================================
    # GENERAL
    # =====================================================

    return handle_general_request(
        message
    )


# =========================================================
# EMAIL REQUEST
# =========================================================

def handle_email_request(message: str):

    """
    Route email requests to the Email Agent.

    The Email Agent/workflow is responsible for
    understanding the specific email action.
    """

    try:

        # Import the workflow dynamically so that
        # master_agent.py does not create a circular
        # import during application startup.

        from workflows.larvi_graph import (
            run_email_workflow
        )

        return run_email_workflow(
            message
        )

    except ImportError:

        # -------------------------------------------------
        # Fallback
        # -------------------------------------------------

        try:

            response = email_agent(
                action="",
                to="",
                subject="",
                body="",
                query="",
                message_id=""
            )

            return {
                "category": "EMAIL",
                "response": response
            }

        except Exception as e:

            print(
                f"Email Agent error: {e}"
            )

            return {
                "category": "EMAIL",
                "response": (
                    "I couldn't process the "
                    "email request."
                )
            }

    except Exception as e:

        print(
            f"Email workflow error: {e}"
        )

        return {
            "category": "EMAIL",
            "response": (
                "I couldn't process the "
                "email request."
            )
        }


# =========================================================
# CALENDAR REQUEST
# =========================================================

def handle_calendar_request(message: str):

    """
    Route calendar requests to the Calendar workflow.
    """

    try:

        from workflows.larvi_graph import (
            run_calendar_workflow
        )

        return run_calendar_workflow(
            message
        )

    except ImportError:

        return {
            "category": "CALENDAR",
            "response": (
                "The calendar workflow is not "
                "available yet."
            )
        }

    except Exception as e:

        print(
            f"Calendar workflow error: {e}"
        )

        return {
            "category": "CALENDAR",
            "response": (
                "I couldn't process the "
                "calendar request."
            )
        }


# =========================================================
# DRIVE REQUEST
# =========================================================

def handle_drive_request(message: str):

    """
    Route Google Drive requests.

    This function is intentionally prepared for
    the Drive Agent.

    Once drive_agent.py is created, uncomment:

        from agents.drive_agent import drive_agent

    and route the request through it.
    """

    try:

        from agents.drive_agent import (
            drive_agent
        )

        response = drive_agent(
            message
        )

        return {
            "category": "DRIVE",
            "response": response
        }

    except ImportError:

        return {
            "category": "DRIVE",
            "response": (
                "Google Drive support is not "
                "connected yet."
            )
        }

    except Exception as e:

        print(
            f"Drive Agent error: {e}"
        )

        return {
            "category": "DRIVE",
            "response": (
                "I couldn't process the "
                "Google Drive request."
            )
        }


# =========================================================
# GENERAL REQUEST
# =========================================================

def handle_general_request(message: str):

    """
    Handle normal conversational questions using
    the LARVI LLM.
    """

    try:

        response = call_ollama([
            {
                "role": "system",
                "content": """
You are LARVI, an intelligent personal AI assistant.

Answer the user's question clearly, naturally,
and helpfully.

You can help with:

- General questions
- Programming
- Learning
- Explanations
- Writing
- Brainstorming
- Everyday tasks

IMPORTANT:

Do not claim that you performed an external action
unless a real LARVI tool successfully performed it.

If Gmail, Calendar, or Google Drive functionality
is required, the appropriate agent should handle
the request.

Never pretend that an external action was completed.
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

    except Exception as e:

        print(
            f"General LARVI error: {e}"
        )

        return {
            "category": "GENERAL",
            "response": (
                "Sorry, I couldn't process "
                "your request right now."
            )
        }


# =========================================================
# SIMPLE ALIAS
# =========================================================

def run_master_agent(message: str):

    """
    Alternative function name for calling the
    Master Agent from FastAPI or other workflows.
    """

    return master_agent(
        message
    )
