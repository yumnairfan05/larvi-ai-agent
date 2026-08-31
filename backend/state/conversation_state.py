# =========================================================
# LARVI CONVERSATION STATE
# =========================================================
#
# Stores short-term conversation context for LARVI.
#
# This allows LARVI to understand follow-up requests such as:
#
# User: Find my Team Meeting
# LARVI: I found your Team Meeting.
#
# User: Move it to 5 PM
#
# LARVI can use the previous event information.
#
# =========================================================


from typing import Optional, Dict, Any


# =========================================================
# CONVERSATION STATE
# =========================================================

class ConversationState:

    def __init__(self):

        # -------------------------------------------------
        # Last detected category
        # -------------------------------------------------

        self.category: str = "GENERAL"

        # -------------------------------------------------
        # Last user message
        # -------------------------------------------------

        self.last_message: str = ""

        # -------------------------------------------------
        # Last assistant response
        # -------------------------------------------------

        self.last_response: str = ""

        # -------------------------------------------------
        # Last action performed
        #
        # Examples:
        #
        # "view"
        # "find"
        # "create"
        # "update"
        # "delete"
        # "read"
        # "send"
        # "search"
        # -------------------------------------------------

        self.last_action: str = ""

        # -------------------------------------------------
        # Last email information
        # -------------------------------------------------

        self.email: Dict[str, Any] = {
            "message_id": "",
            "thread_id": "",
            "from": "",
            "to": "",
            "subject": "",
            "date": "",
            "body": ""
        }

        # -------------------------------------------------
        # Last calendar event information
        # -------------------------------------------------

        self.calendar: Dict[str, Any] = {
            "event_id": "",
            "summary": "",
            "start_time": "",
            "end_time": "",
            "description": "",
            "location": ""
        }

        # -------------------------------------------------
        # Last search query
        # -------------------------------------------------

        self.last_search: str = ""

        # -------------------------------------------------
        # Generic extra information
        # -------------------------------------------------

        self.extra: Dict[str, Any] = {}

    # =====================================================
    # UPDATE STATE
    # =====================================================

    def update(
        self,
        category: Optional[str] = None,
        message: Optional[str] = None,
        response: Optional[str] = None,
        action: Optional[str] = None,
        email: Optional[Dict[str, Any]] = None,
        calendar: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ):

        # -------------------------------------------------
        # Basic conversation information
        # -------------------------------------------------

        if category is not None:
            self.category = category

        if message is not None:
            self.last_message = message

        if response is not None:
            self.last_response = response

        if action is not None:
            self.last_action = action

        if search is not None:
            self.last_search = search

        # -------------------------------------------------
        # Email information
        # -------------------------------------------------

        if email:

            for key, value in email.items():

                if value is not None:
                    self.email[key] = value

        # -------------------------------------------------
        # Calendar information
        # -------------------------------------------------

        if calendar:

            for key, value in calendar.items():

                if value is not None:
                    self.calendar[key] = value

        # -------------------------------------------------
        # Extra information
        # -------------------------------------------------

        if extra:

            self.extra.update(
                extra
            )

    # =====================================================
    # GET EMAIL VALUE
    # =====================================================

    def get_email(
        self,
        key: str,
        default: str = ""
    ):

        return self.email.get(
            key,
            default
        )

    # =====================================================
    # GET CALENDAR VALUE
    # =====================================================

    def get_calendar(
        self,
        key: str,
        default: str = ""
    ):

        return self.calendar.get(
            key,
            default
        )

    # =====================================================
    # GET LAST EVENT ID
    # =====================================================

    def get_last_event_id(self):

        return self.calendar.get(
            "event_id",
            ""
        )

    # =====================================================
    # GET LAST EMAIL ID
    # =====================================================

    def get_last_message_id(self):

        return self.email.get(
            "message_id",
            ""
        )

    # =====================================================
    # CLEAR EMAIL STATE
    # =====================================================

    def clear_email(self):

        self.email = {
            "message_id": "",
            "thread_id": "",
            "from": "",
            "to": "",
            "subject": "",
            "date": "",
            "body": ""
        }

    # =====================================================
    # CLEAR CALENDAR STATE
    # =====================================================

    def clear_calendar(self):

        self.calendar = {
            "event_id": "",
            "summary": "",
            "start_time": "",
            "end_time": "",
            "description": "",
            "location": ""
        }

    # =====================================================
    # CLEAR EVERYTHING
    # =====================================================

    def clear(self):

        self.category = "GENERAL"

        self.last_message = ""

        self.last_response = ""

        self.last_action = ""

        self.last_search = ""

        self.clear_email()

        self.clear_calendar()

        self.extra = {}

    # =====================================================
    # CONVERT TO DICTIONARY
    # =====================================================

    def to_dict(self):

        return {
            "category": self.category,

            "last_message": self.last_message,

            "last_response": self.last_response,

            "last_action": self.last_action,

            "email": self.email.copy(),

            "calendar": self.calendar.copy(),

            "last_search": self.last_search,

            "extra": self.extra.copy()
        }


# =========================================================
# GLOBAL CONVERSATION STATE
# =========================================================
#
# For the current local application, one state object is
# enough to maintain the active conversation.
#
# =========================================================

conversation_state = ConversationState()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_conversation_state():

    return conversation_state


def reset_conversation():

    conversation_state.clear()

    return conversation_state


# =========================================================
# UPDATE CONVERSATION
# =========================================================

def update_conversation(
    category=None,
    message=None,
    response=None,
    action=None,
    email=None,
    calendar=None,
    search=None,
    extra=None
):

    conversation_state.update(
        category=category,
        message=message,
        response=response,
        action=action,
        email=email,
        calendar=calendar,
        search=search,
        extra=extra
    )

    return conversation_state


# =========================================================
# GET LAST EVENT
# =========================================================

def get_last_calendar_event():

    return conversation_state.calendar.copy()


# =========================================================
# GET LAST EMAIL
# =========================================================

def get_last_email():

    return conversation_state.email.copy()
