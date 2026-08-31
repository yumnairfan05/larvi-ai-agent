from tools.gmail_tools import get_unread_emails


emails = get_unread_emails(max_results=5)

print("\nUnread emails:\n")

if not emails:
    print("No unread emails found.")

else:
    for email in emails:
        print("--------------------------------")
        print("From:", email["from"])
        print("Subject:", email["subject"])
        print("Date:", email["date"])