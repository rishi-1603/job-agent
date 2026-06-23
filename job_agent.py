import os

print("Job Agent Started")

email_user = os.getenv("EMAIL_USER")

print(f"Email configured: {email_user}")
