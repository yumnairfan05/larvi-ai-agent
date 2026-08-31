from services.google_service import (
    get_gmail_service,
    get_calendar_service
)

print("Testing Gmail...")

gmail = get_gmail_service()

profile = gmail.users().getProfile(
    userId="me"
).execute()

print("Gmail connected:", profile["emailAddress"])


print("Testing Calendar...")

calendar = get_calendar_service()

calendar_list = calendar.calendarList().list().execute()

print(
    "Calendar connected:",
    len(calendar_list.get("items", [])),
    "calendar(s)"
)