from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64
import schedule
import time


import os
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no valid credentials, go through the authentication flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def send_email(recipient, subject, body):
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(body)
    message['to'] = recipient
    message['from'] = 'your-email@gmail.com'
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {'raw': raw}
    service.users().messages().send(userId="me", body=message_body).execute()


def categorize_emails(query):
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_id = msg['id']
        service.users().messages().modify(
            userId='me', id=msg_id,
            body={'addLabelIds': ['IMPORTANT']}
        ).execute()


def schedule_email(recipient, subject, body, send_time):
    def send_scheduled_email():
        send_email(recipient, subject, body)
    schedule.every().day.at(send_time).do(send_scheduled_email)

    while True:
        schedule.run_pending()
        time.sleep(1)


