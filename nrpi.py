from __future__ import print_function
import datetime
from datetime import timedelta
import pickle
import os.path
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
dietpi = 'http://localhost:5000/'
tokenPickle = "/home/dietpi/projects/cmon-baby-light-my-pi/token.pickle"
credentialsFile = '/home/dietpi/projects/cmon-baby-light-my-pi/credentials.json'


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tokenPickle):
        with open(tokenPickle, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsFile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenPickle, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow()
    next = now + timedelta(minutes=1)
    #print(now + " --- " + next.isoformat() + 'Z')
    #print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now.isoformat() + 'Z', timeMax=next.isoformat() + 'Z',
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print(now.isoformat() + 'Z'  + ' No upcoming events found.')
        r = requests.get(dietpi + 'green')
    if len(events) > 0:
        r = requests.get(dietpi + 'red')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    
    #for event in events:
    #    start = event['start'].get('dateTime', event['start'].get('date'))
    #    print(start, event['summary'])
    #    r = requests.get(dietpi + 'red')


if __name__ == '__main__':
    main()
