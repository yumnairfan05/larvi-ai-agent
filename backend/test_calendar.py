from tools.calendar_tools import create_calendar_event


result = create_calendar_event(
    summary="LARVI Test Meeting",
    start_time="2026-08-27T15:00:00",
    end_time="2026-08-27T15:30:00",
    description="Test event created through the LARVI Google Calendar API.",
    location=""
)

print(result)