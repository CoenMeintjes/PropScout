from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2.credentials import Credentials

# creds = Credentials.from_authorized_user_info(info={
#     'client_id': '613195364254-tlroi9l83743fs655taajo3jj206hncp.apps.googleusercontent.com',
#     'client_secret': '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',
#     'refresh_token': 'your-refresh-token',
#     'token_uri': 'https://oauth2.googleapis.com/token',
#     'redirect_uri': 'http://localhost'
# })


# Set up the credentials for accessing the Gmail API
creds = Credentials.from_authorized_user_file('C:/Users/Margie/Documents/02_Programming/Python/Projects/PropScout/credentials2.json', ['https://www.googleapis.com/auth/gmail.readonly'])
service = build('gmail', 'v1', credentials=creds)

# Define a function to retrieve the emails from the specified inbox folder
def get_emails_from_folder(folder_name):
    try:
        folder = service.users().labels().get(userId='me', id=folder_name).execute()
        messages = service.users().messages().list(userId='me', labelIds=[folder['id']]).execute().get('messages', [])
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            print(msg['payload']['body']['data'])
    except HttpError as error:
        print(f"An error occurred: {error}")

get_emails_from_folder('INBOX/02_Property')

print(get_emails_from_folder)
