import os
import csv
import re
import pytz  # Import 'pytz' for handling timezones
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Output CSV file name
CSV_FILE = 'calendar_emails.csv'
# Your Google Calendar API credentials (JSON file) and calendar ID
SERVICE_ACCOUNT_FILE = ''
CALENDAR_ID = ''

def main():
    # Set up the credentials using the service account JSON key file
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/calendar.readonly']
    )

    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)

    # Calculate the start and end dates for the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Initialize a dictionary to store email information
    email_info = {}

    # Use pagination to retrieve all events
    page_token = None
    while True:
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            singleEvents=True,
            timeMin=start_date.isoformat() + 'Z',
            timeMax=end_date.isoformat() + 'Z',
            pageToken=page_token
        ).execute()
        events = events_result.get('items', [])
        # Define a UTC timezone object
        utc = pytz.utc
        for event in events:
            attendees = event.get('attendees', [])
            for attendee in attendees:
                email = attendee.get('email')
                if email:
                    if email not in email_info:
                        email_info[email] = {'meeting_count': 0, 'first_meeting_date': datetime.now(utc)}

                    email_info[email]['meeting_count'] += 1

                    # Ensure the timezone offset part has two digits for minutes
                    start_time = event.get('start', {}).get('dateTime')  # Check if 'start' contains 'dateTime'
                    if start_time:
                        iso_datetime_str = re.sub(r'([+-]\d{2})(\d{2})$', r'\1:\2', start_time)
                        meeting_date = datetime.fromisoformat(iso_datetime_str).replace(tzinfo=pytz.utc)

                        if meeting_date < email_info[email]['first_meeting_date']:
                            email_info[email]['first_meeting_date'] = meeting_date
        page_token = events_result.get('nextPageToken')
        if not page_token:
            break

    if not email_info:
        print('No events found in your calendar for the past year.')
    else:
        # Write email addresses, meeting counts, and first meeting dates to a CSV file
        with open(CSV_FILE, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Email', 'Meeting Count', 'First Meeting Date'])
            for email, info in email_info.items():
                csvwriter.writerow([email, info['meeting_count'], info['first_meeting_date'].strftime('%Y-%m-%d')])

        print(f'Emails of people you\'ve had events with in the past year, along with their meeting counts and first meeting dates, have been saved to "{CSV_FILE}".')

if __name__ == '__main__':
    main()
