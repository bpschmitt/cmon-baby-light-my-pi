from __future__ import print_function
import datetime
from datetime import timedelta
import pickle
import os.path
import requests
import logging
from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
today = datetime.datetime.date(datetime.datetime.now())
dietpi = 'http://localhost:5000/'
tokenPickle = "/home/dietpi/projects/cmon-baby-light-my-pi/token.pickle"
credentialsFile = '/home/dietpi/projects/cmon-baby-light-my-pi/credentials.json'
logFile = '/tmp/pi.' + str(today) + '.log'
colorList = {'5': 'yellow','9': 'blue', '10': 'green', '11': 'red'}
startTime, endTime = 8, 18

#################################################################################

logger = logging.getLogger('nrpi')
handler = logging.FileHandler(logFile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#logger.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def setColor(events):

    today = datetime.datetime.now()

    if today.strftime('%A') == 'Saturday' or today.strftime('%A') == 'Sunday':
        r = requests.get(dietpi + 'off')
        logger.info('It\'s the weekend.')
    elif int(today.strftime('%H')) < startTime  or int(today.strftime('%H')) >= endTime:
        r = requests.get(dietpi + 'off')
        logger.info('It\'s after hours.')
    else:
        if not events:
            logger.info('No events found.')
            r = requests.get(dietpi + 'green')
        else:
            for event in events:
                if 'colorId' in event:
                    color = colorList[event['colorId']]
                    r = requests.get(dietpi + color)
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    logger.info('eventStartTime: ' + start + ' - eventTitle: ' + event['summary'] + ' - eventColor: ' + color)
                else:
                    color = 'red'
                    r = requests.get(dietpi + color)
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    logger.info('eventStartTime: ' + start + ' - eventTitle: ' + event['summary'] + ' - eventColor: ' + color)


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

    events_result = service.events().list(calendarId='primary',
                                        timeMin=now.isoformat() + 'Z', timeMax=next.isoformat() + 'Z',
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    setColor(events)
 
if __name__ == '__main__':
    main()
