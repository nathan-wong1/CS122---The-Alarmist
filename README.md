# CS122-The Alarmist

**Members:**

● Nathan Wong (nathan.s.wong@sjsu.edu)

● Fnu Hasham (fnu.hasham@sjsu.edu)

## Introduction

We created an alarm GUI application that incorporates aspects from Google Calendar and the mobile alarm app.  Currently, for Google and Apple’s Calendar application, there is no official alarm that goes off to remind the user of an event or task that needs to be completed.  While the user can receive notifications from the Calendar app, what happens if the user turns on Do Not Disturb and silences all notifications.  They could, in theory, set an alarm in the “Clock” app with a label of the task or event, however, the alarm can only be set up 24 hours in advance.  This is a massive drawback of the Clock app because most meetings in the workplace and businesses are set up days or even months in advance.  Our goal is to build an application that combines the essential features from both platforms.

## Setting Up Enviroment

1. Download the project zip file
2. In File Explorer, find the project and unzip the downloaded zipped file
3. Open an IDE like Visual Studios or Pycharm (Python 3.12 recommended)
4. Download the following modules in local terminal:
    - pip install FreeSimpleGUI
    - pip install PyQt5
5. Open the main.py file and run the file
   
   OR

   Right click main.py > Run 'main'

6. Application should be executed and running

### Notes: 

- Module winsound only works on Windows operating systems, NOT Mac/Linux
- Duplicate alarms can exist
- Alarms can be set in the past
- Alarms do not have to have descriptions
- There is a very slight delay (10ms max) when Timer class updates the countdown timer
- Timers can run concurrently while user is in another view

