"""
Blitz Gmail Draft Sender
Saves any HTML email directly to Gmail Drafts via the Gmail API.
Run: python3 gmail_draft_sender.py
"""

import os, base64, json, pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
CREDS_FILE  = os.path.expanduser("blitz_gmail_credentials.json")
TOKEN_FILE  = os.path.expanduser("~/blitz_gmail_token.pickle")
EMAILS_DIR  = os.path.dirname(os.path.abspath(__file__))


def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_FILE):
                print("\n❌  credentials.json not found.")
                print("    Follow the setup steps printed below.\n")
                print_setup_instructions()
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return build("gmail", "v1", credentials=creds)


def create_draft(service, subject, html_body, to=""):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = "me"
    msg["To"]      = to
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    draft = service.users().drafts().create(
        userId="me",
        body={"message": {"raw": raw}}
    ).execute()
    return draft


def save_email_as_draft(html_file, subject, to=""):
    service = get_gmail_service()
    if not service:
        return

    html_path = os.path.join(EMAILS_DIR, html_file)
    with open(html_path, "r", encoding="utf-8") as f:
        html_body = f.read()

    draft = create_draft(service, subject, html_body, to)
    print(f"\n✅  Draft saved to Gmail!")
    print(f"    Subject : {subject}")
    print(f"    Draft ID: {draft['id']}")
    print(f"    Open Gmail → Drafts to find it.\n")


def print_setup_instructions():
    print("=" * 60)
    print("  ONE-TIME SETUP — takes ~3 minutes")
    print("=" * 60)
    print("""
1. Go to: https://console.cloud.google.com/
2. Create a new project  (top-left dropdown → New Project)
3. Search for "Gmail API" → Enable it
4. Go to: APIs & Services → Credentials
5. Click "Create Credentials" → OAuth client ID
6. Application type: Desktop app  → Name: Blitz Drafts → Create
7. Click the download icon (⬇) next to the credential
8. Rename the downloaded file to:  blitz_gmail_credentials.json
9. Move it to your home folder:    ~/blitz_gmail_credentials.json
10. Run this script again — a browser window will open to authorize.
    Sign in with sachin.verma@blitznow.in and allow access.
    After that, drafts are saved automatically — no browser needed.
""")
    print("=" * 60)


if __name__ == "__main__":
    emails = [
        {
            "file":    "blitz_5pm_sameday_email_improved.html",
            "subject": "Your customers ordered at 4 PM. They got it by 9 PM. Here's how.",
            "to":      "",   # ← add recipient email here, or leave blank
        },
    ]

    service = get_gmail_service()
    if not service:
        raise SystemExit(1)

    for e in emails:
        html_path = os.path.join(EMAILS_DIR, e["file"])
        with open(html_path, "r", encoding="utf-8") as f:
            html_body = f.read()
        draft = create_draft(service, e["subject"], html_body, e["to"])
        print(f"✅  Draft saved → \"{e['subject'][:55]}...\"  (ID: {draft['id']})")

    print("\nAll done. Open Gmail → Drafts folder.\n")
