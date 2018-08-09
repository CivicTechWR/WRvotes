#!/usr/bin/env python3
"""
Take events.csv and put it into a Google calendar, using 
patching to update event info. 

Paul "Worthless" Nijjar, 2018-08-08
"""

import csv
import unicodedata
import datetime
import json

# Should be generated as a service account .json file
# in console.developers.google.com .
#
# This account needs access to the Google Calendar API. 
# It needs the ability to edit the calendar in question.
SERVICE_CREDENTIALS="./secrets/service-account-credentials.json"

with open(SERVICE_CREDENTIALS) as f:
    calendar_bot = json.load(f)

