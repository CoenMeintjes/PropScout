#!/usr/bin/env python

import os.path
import base64
import pprint
import sqlite3
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.parse import urlparse
import ssl
from bs4 import BeautifulSoup
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('property_analysis_db.sqlite')
cur = conn.cursor()

# Create the tables using executescript()
cur.executescript('''
CREATE TABLE IF NOT EXISTS Urls (
    id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
    url     TEXT UNIQUE,
    html    TEXT,
    json    TEXT,
    parsed  INTEGER
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
        creds.token_expiry = datetime.datetime.now() + datetime.timedelta(hours=25)  # Set token expiration time to 25 hours
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    # Initial Call of the Gmail API results in dict() of messages IDs that conform to parameters LIMITED to 50 
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', q='in:INBOX/02_Property/analysis_alerts', maxResults=50).execute()

    messages = results.get('messages', [])
    
    # Iterate through the pulled messages and extract the relevant information to parse to SQLite
    # A second api call is made to retrieve all of the message data using get() method. 
    # Returns a dictionary containing detailed information about the message stored in msg
    # Email bodies are encoded so this is parsed with base64 lib 
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        body = msg.get('payload', {}).get('body', {}).get('data', '') # using dict.get() method to access nested dictionary values without raising a KeyError if no key
        decode_body =base64.urlsafe_b64decode(body.encode('UTF-8')).decode('UTF-8')
        soup = BeautifulSoup(decode_body, "html.parser")
        tags = soup('a')

        # iterate trough the tags and extract links to the listing link
        # insert these into the table URLs amd commit when done
        for tag in tags:
            href = tag.get('href', None)
            if href and 'RedirectToListing' in href:
                # use try except to avoid being stopped by url error
                try:
                    fetch = urlopen(href)
                    html = fetch.read()
                    # soup = BeautifulSoup(html, "html.parser")
                    cur.execute('''INSERT OR IGNORE INTO Urls (url, html)
                                VALUES ( ?, ? )''', ( href, html ) )
                except:
                    continue
        conn.commit()

    # Print out the links that have been added to the DB
    cur.execute('SELECT id, url, parsed FROM Urls ORDER BY id ASC')
    rows = cur.fetchall() 
    for row in rows:
        if row[2] is None: # checking if the parsed value is 0 (parsed column index is [2])
            print(row)
    
    if not messages:
        print('No messages found.')
    
except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f'An error occurred: {error}')

