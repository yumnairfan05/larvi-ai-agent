from tools.gmail_tools import send_email


result = send_email(
    to="yumnaaries0504@gmail.com",
    subject="LARVI Test Email",
    body="Hello! This is a test email sent through LARVI's Gmail API integration."
)

print(result)