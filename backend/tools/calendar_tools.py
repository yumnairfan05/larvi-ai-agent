from datetime import datetime, timezone

from services.google_service import get_calendar_service


# =========================================================
# GET UPCOMING EVENTS
# =========================================================

def get_upcoming_events(max_results: int = 10):

    try:

        service = get_calendar_service()

        now = datetime.now(timezone.utc).isoformat()

        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get(
            "items",
            []
        )

        results = []

        for event in events:

            start = event.get(
                "start",
                {}
            )

            start_time = (
                start.get("dateTime")
                or start.get("date")
                or ""
            )

            results.append({
                "id": event.get("id"),
                "summary": event.get(
                    "summary",
                    ""
                ),
                "start": start_time,
                "description": event.get(
                    "description",
                    ""
                ),
                "location": event.get(
                    "location",
                    ""
                )
            })

        return results

    except Exception as e:

        print(
            f"Calendar upcoming events error: {e}"
        )

        return []


# =========================================================
# FIND CALENDAR EVENTS
# =========================================================

def find_calendar_events(
    search_text: str,
    max_results: int = 10
):

    try:

        service = get_calendar_service()

        now = datetime.now(
            timezone.utc
        ).isoformat()

        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
            q=search_text
        ).execute()

        events = events_result.get(
            "items",
            []
        )

        results = []

        for event in events:

            results.append({
                "id": event.get("id"),
                "summary": event.get(
                    "summary",
                    ""
                ),
                "start": event.get(
                    "start",
                    {}
                ),
                "end": event.get(
                    "end",
                    {}
                ),
                "description": event.get(
                    "description",
                    ""
                ),
                "location": event.get(
                    "location",
                    ""
                )
            })

        return results

    except Exception as e:

        print(
            f"Calendar search error: {e}"
        )

        return []


# =========================================================
# CHECK AVAILABILITY
# =========================================================

def check_calendar_availability(
    start_time: str,
    end_time: str
):

    try:

        service = get_calendar_service()

        start_datetime = datetime.fromisoformat(
            start_time
        )

        end_datetime = datetime.fromisoformat(
            end_time
        )

        # Convert to UTC for Google Calendar API
        start_utc = start_datetime.astimezone(
            timezone.utc
        ).isoformat()

        end_utc = end_datetime.astimezone(
            timezone.utc
        ).isoformat()

        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_utc,
            timeMax=end_utc,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get(
            "items",
            []
        )

        conflicts = []

        for event in events:

            event_start = event.get(
                "start",
                {}
            )

            event_end = event.get(
                "end",
                {}
            )

            event_start_time = (
                event_start.get("dateTime")
                or event_start.get("date")
                or ""
            )

            event_end_time = (
                event_end.get("dateTime")
                or event_end.get("date")
                or ""
            )

            conflicts.append({
                "id": event.get(
                    "id"
                ),
                "summary": event.get(
                    "summary",
                    ""
                ),
                "start": event_start_time,
                "end": event_end_time
            })

        return {
            "success": True,
            "available": len(conflicts) == 0,
            "conflicts": conflicts
        }

    except Exception as e:

        return {
            "success": False,
            "available": False,
            "conflicts": [],
            "error": str(e)
        }


# =========================================================
# CREATE CALENDAR EVENT
# =========================================================

def create_calendar_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str = "",
    location: str = ""
):

    try:

        service = get_calendar_service()

        event = {
            "summary": summary,
            "description": description,
            "location": location,
            "start": {
                "dateTime": start_time,
                "timeZone": "Asia/Karachi"
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Asia/Karachi"
            }
        }

        created_event = service.events().insert(
            calendarId="primary",
            body=event
        ).execute()

        return {
            "success": True,
            "event_id": created_event.get(
                "id"
            ),
            "event_link": created_event.get(
                "htmlLink"
            ),
            "summary": created_event.get(
                "summary"
            ),
            "start": created_event.get(
                "start"
            ),
            "end": created_event.get(
                "end"
            )
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# UPDATE CALENDAR EVENT
# =========================================================

def update_calendar_event(
    event_id: str,
    summary: str = None,
    start_time: str = None,
    end_time: str = None,
    description: str = None,
    location: str = None
):

    try:

        service = get_calendar_service()

        event = service.events().get(
            calendarId="primary",
            eventId=event_id
        ).execute()

        if summary is not None:
            event["summary"] = summary

        if description is not None:
            event["description"] = description

        if location is not None:
            event["location"] = location

        if start_time is not None:

            event["start"] = {
                "dateTime": start_time,
                "timeZone": "Asia/Karachi"
            }

        if end_time is not None:

            event["end"] = {
                "dateTime": end_time,
                "timeZone": "Asia/Karachi"
            }

        updated_event = service.events().update(
            calendarId="primary",
            eventId=event_id,
            body=event
        ).execute()

        return {
            "success": True,
            "event_id": updated_event.get(
                "id"
            ),
            "event_link": updated_event.get(
                "htmlLink"
            ),
            "summary": updated_event.get(
                "summary"
            )
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# DELETE CALENDAR EVENT
# =========================================================

def delete_calendar_event(
    event_id: str
):

    try:

        service = get_calendar_service()

        service.events().delete(
            calendarId="primary",
            eventId=event_id
        ).execute()

        return {
            "success": True,
            "message": (
                "Calendar event deleted successfully."
            )
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
