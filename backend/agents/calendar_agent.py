from tools.calendar_tools import (
    get_upcoming_events,
    find_calendar_events,
    check_calendar_availability,
    create_calendar_event,
    update_calendar_event,
    delete_calendar_event,
)


# =========================================================
# VIEW EVENTS
# =========================================================

def handle_view_events():

    events = get_upcoming_events(
        max_results=10
    )

    if not events:

        return (
            "You don't have any upcoming "
            "calendar events."
        )

    response = (
        "Here are your upcoming events:\n\n"
    )

    for index, event in enumerate(
        events,
        start=1
    ):

        response += (
            f"{index}. {event['summary']}\n"
            f"Start: {event['start']}\n"
        )

        if event["location"]:

            response += (
                f"Location: "
                f"{event['location']}\n"
            )

        response += "\n"

    return response


# =========================================================
# FIND EVENTS
# =========================================================

def handle_find_event(
    search_text: str
):

    if not search_text:

        return (
            "Please tell me which event "
            "you're looking for."
        )

    events = find_calendar_events(
        search_text,
        max_results=10
    )

    if not events:

        return (
            f"I couldn't find an upcoming event "
            f"matching '{search_text}'."
        )

    response = (
        "I found these matching events:\n\n"
    )

    for index, event in enumerate(
        events,
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
            f"Start: {start_time}\n"
            f"Event ID: "
            f"{event.get('id')}\n\n"
        )

    return response


# =========================================================
# CHECK AVAILABILITY
# =========================================================

def handle_check_availability(
    start_time: str,
    end_time: str
):

    if not start_time:

        return (
            "Please provide the start time "
            "to check availability."
        )

    if not end_time:

        return (
            "Please provide the end time "
            "to check availability."
        )

    result = check_calendar_availability(
        start_time=start_time,
        end_time=end_time
    )

    if not result.get("success"):

        return (
            "I couldn't check your calendar "
            "availability.\n"
            f"Error: {result.get('error', '')}"
        )

    if result.get("available"):

        return (
            "You are available during "
            f"{start_time} to {end_time}."
        )

    response = (
        "You are not available during "
        f"{start_time} to {end_time}.\n\n"
        "Conflicting events:\n\n"
    )

    for index, conflict in enumerate(
        result.get("conflicts", []),
        start=1
    ):

        response += (
            f"{index}. "
            f"{conflict.get('summary', '')}\n"
            f"Start: "
            f"{conflict.get('start', '')}\n"
            f"End: "
            f"{conflict.get('end', '')}\n\n"
        )

    return response


# =========================================================
# CREATE EVENT
# =========================================================

def handle_create_event(
    summary,
    start_time,
    end_time,
    description="",
    location=""
):

    if not summary:

        return "Please provide an event title."

    if not start_time:

        return "Please provide a start time."

    if not end_time:

        return "Please provide an end time."

    result = create_calendar_event(
        summary=summary,
        start_time=start_time,
        end_time=end_time,
        description=description,
        location=location
    )

    if result.get("success"):

        return (
            "Calendar event created successfully.\n"
            f"Event: {result.get('summary', '')}"
        )

    return (
        "I couldn't create the calendar event.\n"
        f"Error: {result.get('error', '')}"
    )


# =========================================================
# UPDATE EVENT
# =========================================================

def handle_update_event(
    event_id,
    summary=None,
    start_time=None,
    end_time=None,
    description=None,
    location=None
):

    if not event_id:

        return (
            "I couldn't determine which "
            "event to update."
        )

    result = update_calendar_event(
        event_id=event_id,
        summary=summary,
        start_time=start_time,
        end_time=end_time,
        description=description,
        location=location
    )

    if result.get("success"):

        return (
            "Calendar event updated successfully.\n"
            f"Event: {result.get('summary', '')}"
        )

    return (
        "I couldn't update the calendar event.\n"
        f"Error: {result.get('error', '')}"
    )


# =========================================================
# DELETE EVENT
# =========================================================

def handle_delete_event(
    event_id
):

    if not event_id:

        return (
            "I couldn't determine which "
            "event to delete."
        )

    result = delete_calendar_event(
        event_id
    )

    if result.get("success"):

        return (
            "Calendar event deleted successfully."
        )

    return (
        "I couldn't delete the calendar event.\n"
        f"Error: {result.get('error', '')}"
    )


# =========================================================
# CALENDAR AGENT
# =========================================================

def calendar_agent(
    action,
    summary="",
    start_time="",
    end_time="",
    description="",
    location="",
    event_id="",
    search_text=""
):

    action = action.lower().strip()

    # -----------------------------------------------------
    # VIEW
    # -----------------------------------------------------

    if action == "view":

        return handle_view_events()

    # -----------------------------------------------------
    # FIND
    # -----------------------------------------------------

    if action == "find":

        return handle_find_event(
            search_text
        )

    # -----------------------------------------------------
    # CHECK AVAILABILITY
    # -----------------------------------------------------

    if action == "check":

        return handle_check_availability(
            start_time=start_time,
            end_time=end_time
        )

    # -----------------------------------------------------
    # CREATE
    # -----------------------------------------------------

    if action == "create":

        return handle_create_event(
            summary=summary,
            start_time=start_time,
            end_time=end_time,
            description=description,
            location=location
        )

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    if action == "update":

        return handle_update_event(
            event_id=event_id,
            summary=summary or None,
            start_time=start_time or None,
            end_time=end_time or None,
            description=description or None,
            location=location or None
        )

    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------

    if action == "delete":

        return handle_delete_event(
            event_id
        )

    return (
        "I don't recognize that calendar action."
    )
