### Quick calendar analyics
This tutorial is for non-engineers, and should take no more than 5 minutes. 

#### Step 1: Fill in lines 12 & 13 in rolodex.py
Go to the [Google Cloud Console](https://console.cloud.google.com/). Click on the project drop-down and select or create the project for which you want to create service account credentials. 

- __Enable the Google Calendar API__: In the Google Cloud Console, navigate to the "APIs & Services" > "Library" page. Use the search bar to find the "Google Calendar API" and click on it. Click the "Enable" button to enable the API for your project.
- __Create a Service Account__:
In the Google Cloud Console, navigate to the "APIs & Services" > "Credentials" page.
Click the "Create credentials" button and select "Service Account Key."
Choose a name for your service account and assign it a role (e.g., "Project" > "Editor" role).
For the key type, select "JSON" and click the "Create" button. This will download the service account credentials as a JSON file to your computer.
- __Share Google Calendar with Service Account Email__:
After creating the service account, you'll see an email address associated with the service account (ending in @<project-id>.iam.gserviceaccount.com). [Share your Google Calendar with this email address](https://support.google.com/calendar/answer/37082?hl=en) and grant it the necessary permissions, "Read" access, so it can access your calendar data.
- __Line 12__: Use Service Account Credentials in Your Script:
Put the .json file in the same folder as the code you downloaded. In line 12 of rolodex.py, put the name of this JSON file.
- __Line 13__: Go to Google Calendar and make sure you are logged in with the Google account associated with the calendar you want to access. In the left sidebar, click on the gear icon (⚙️) to open the Calendar settings. Under "Settings for my calendars," you'll see a list of your calendars. Choose the calendar you want to access. To get the Calendar ID, scroll down to the "Integrate calendar" section for the selected calendar. In the "Calendar ID" section, you will find the CALENDAR_ID. It will look something like an email address but is unique to your calendar and has the format: example@gmail.com or example@group.calendar.google.com.

#### Step 2: Install requirements & run script
Go to your terminal and run the following

`cd ~/Downloads/calendar-analysis`

`pip -r requirements.txt`

`python rolodex.py`

Enjoy ☕️ 📆
