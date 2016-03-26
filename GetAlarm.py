from __future__ import print_function
import httplib2
import os
from alarms import alarms
import time
import dateutil.parser
import pytz

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.client import SignedJwtAssertionCredentials
import datetime
from datetime import timedelta

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


class GetAlarm:
    alarmSummary = ""
    alarmTime = ""
    service = ""
    def __init__(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        http = credentials.authorize(httplib2.Http())


        self.service = discovery.build('calendar', 'v3', http=http)




    def getAlarm(self):
        lalarms = []
        cest = pytz.timezone('America/New_York')
        now = datetime.datetime.now(tz=cest)
        timeMiner = datetime.datetime(year=now.year, month=now.month, day=now.day, hour = now.hour, minute = now.minute, second = now.second, tzinfo=cest) + timedelta(minutes=1)
        timeMiner = timeMiner.isoformat()
        print(timeMiner)
        print('Getting the upcoming 10 events')
        calendar_list = self.service.events().list(calendarId='7sct8jgf8nlfvmc20n8eag4nnk@group.calendar.google.com', fields="items(start,summary)", singleEvents = True, orderBy="startTime", timeMin = timeMiner, maxResults = "6").execute()


        dateOld = " "
        index = 0
        if not calendar_list:
            print('No upcoming events found.')
        
        for event in calendar_list['items']:
            if index <= 2:
                if dateOld != dateutil.parser.parse(event['start']['dateTime'],ignoretz=True).time():
                    dateOld = dateutil.parser.parse(event['start']['dateTime'],ignoretz=True).time()
                    start = dateutil.parser.parse(event['start']['dateTime'],ignoretz=True)
                    lalarms.append(alarms(event["summary"],start))
                    index += 1

    
        return lalarms
            

