import sys
import json
import smtplib
from email.message import EmailMessage
from datetime import datetime

# ----- CONFIG -----
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "personal.email@gmail.com"
EMAIL_PASSWORD = "app_password"   # move to env var later
EMAIL_TO = "something@gmail.com"
# ------------------

def send_email(subject: str, message_body: str, email_to: list[str], email_user: str, email_password: str) -> None:
    msg = EmailMessage()
    msg["From"] = email_user
    msg["To"] = email_to
    msg["Subject"] = subject

    msg.set_content(
        f"""Automatic shutdown initiated.

Message:
{message_body}

Time:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
        server.starttls()
        server.login(email_user, email_password)
        server.send_message(msg)

def main() -> int:
    subject = sys.argv[1] if len(sys.argv) > 1 else "LabVIEW Alert"
    message_body = sys.argv[2] if len(sys.argv) > 2 else "No message provided"
    email_to_str = sys.argv[3] if len(sys.argv) > 3 else EMAIL_TO
    email_user = sys.argv[4] if len(sys.argv) > 4 else EMAIL_USER
    email_password = sys.argv[5] if len(sys.argv) > 5 else EMAIL_PASSWORD
    
    # Parse comma-separated email addresses
    email_to = [addr.strip() for addr in email_to_str.split(",")]
    
    # Use config defaults if arguments are empty
    email_user = email_user if email_user else EMAIL_USER
    email_password = email_password if email_password else EMAIL_PASSWORD

    try:
        send_email(subject, message_body, email_to, email_user, email_password)

        # stdout: machine-readable success
        print(json.dumps({
            "ok": True,
            "subject": subject,
            "time": datetime.now().isoformat()
        }))
        return 0

    except Exception as e:
        # stderr: machine-readable failure
        print(json.dumps({
            "ok": False,
            "error": type(e).__name__,
            "message": str(e)
        }), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
