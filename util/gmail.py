# Google Imports
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Date util
from dateutil import parser

from bs4 import BeautifulSoup

import base64
import os.path

# Authenticate gmail

def authenticate():
    SCOPES = ['https://mail.google.com/']
    creds = None
    if os.path.exists('tokens/token_gmail.json'):
        creds = Credentials.from_authorized_user_file('tokens/token_gmail.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'tokens/credentials_gmail.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('tokens/token_gmail.json', 'w') as token:
                token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

# Search needed messages

def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    if not messages:
        print('No messages found with the given query:', query)
    return messages

# get message data

def read_message(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get('headers')
    email_id = message['id']
    if headers:
        for header in headers:
            name = header.get('name')
            value = header.get('value')
            if name.lower() == 'from':
                email_sender = value
            if name.lower() == 'subject':
                email_subject = value
            if name.lower() == 'date':
                email_date = parser.parse(value).strftime('%d/%m/%Y %H:%M:%S')
    try:
        parts = payload.get('parts')
        body_html = ''
        for part in parts:
            body = part.get('body')
            data = body.get('data')
            mimeType = part.get('mimeType')
            
            # with attachment
            if mimeType == 'multipart/alternative':
                subparts = part.get('parts')
                for p in subparts:
                    body = p.get('body')
                    data = body.get('data')
                    mimeType = p.get('mimeType')
                    if mimeType == 'text/html':
                        body_html = base64.urlsafe_b64decode(data)
                    elif mimeType == 'text/plain':
                        body_message = base64.urlsafe_b64decode(data)
                    
            # without attachment
            elif mimeType == 'text/html':
                body_html = base64.urlsafe_b64decode(data)
            elif mimeType == 'text/plain':
                body_message = base64.urlsafe_b64decode(data)
        soup = BeautifulSoup(body_html, 'html.parser')
        email_body_plain = str(body_message, 'utf-8')
        email_body_html = str(soup.prettify(formatter='html'))
    except:
        print('Could not get email body')
    message = service.users().messages().modify(userId='me', id=email_id, body={'removeLabelIds': ['UNREAD']}).execute()
    return email_subject, email_sender, email_date, email_body_plain, email_body_html