#!/usr/bin/env python

import os.path
import base64
import pprint
import sqlite3

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

conn = sqlite3.connect('parsed_links.sqlite')
cur = conn.cursor()

# Create the tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Urls;

CREATE TABLE Urls (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    url    TEXT UNIQUE
)
''')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    # Initial Call of the Gmail API results in dict() of messages IDs that conform to parameters
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', q='from: property24', maxResults=10).execute()
    messages = results.get('messages', [])
    
    # Iterate through the pulled messages and extract the relevant information to parse to SQLite
    # A second api call is made to retrieve all of the message data using get() method. 
    # Returns a dictionary containing detailed information about the message stored in msg
    # Email bodies are encoded so this is parsed with base64 lib 
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        body = msg['payload']['body']['data']
        decode_body =base64.urlsafe_b64decode(body.encode('UTF-8')).decode('UTF-8')
        soup = BeautifulSoup(decode_body, "html.parser")
        tags = soup('a')

        # iterate trough the tags and extract links to the listing link
        # insert these into the table URLs amd commit when done
        for tag in tags:
            href = tag.get('href', None)
            if href and 'RedirectToListing' in href:
                cur.execute('''INSERT OR IGNORE INTO Urls (url)
                             VALUES ( ? )''', ( href, ) )
        conn.commit()

    # Print out the links that have been added to the DB
    # TODO - this is currently printing all rows so need to update to only show lastest
    cur.execute('SELECT id, url FROM Urls ORDER BY id DESC')
    rows = cur.fetchall() 
    for row in rows:
        print(row)
    
    if not messages:
        print('No messages found.')
    
except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f'An error occurred: {error}')

