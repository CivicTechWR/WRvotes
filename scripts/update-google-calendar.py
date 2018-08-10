#!/usr/bin/env python3
"""
Take events.csv and put it into a Google calendar, using 
patching to update event info. 

Paul "Worthless" Nijjar, 2018-08-08
"""

import csv, json
import argparse, sys, os
import pprint
import dateutil.parser
from google.oauth2 import service_account
import googleapiclient.discovery

# '/home/pnijjar/watcamp/python_rss/gcal_helpers/config.py'
# See: http://www.karoltomala.com/blog/?p=622
DEFAULT_CONFIG_SOURCEFILE = os.path.join(
    os.getcwd(),
    'update-google-calendar.config.py',
    )

events_dict = {}
positions_dict = {}

script_operation = None

# -----------------------------
def get_padded_id(id_str):
    """ Get the padded calendar ID for Google calendar, 
        because IDs must be at least 5 chars long
    """
    return "00000{}".format(id_str)

# ------------------------------
def get_datetime(datetime_str):
   """ Convert a date/time string that might have a space
      to one that Google will accept.
   """
   d = dateutil.parser.parse(datetime_str)
   return d.strftime("%FT%T")

# ------------------------------
def load_config(configfile=None):
    """ Load configuration definitions.
       (This is really scary, actually. We are trusting that the 
       config.py we are taking as input is sane!) 

       If both the commandline and the parameter are 
       specified then the commandline takes precedence.

       Stolen from my google calendar helpers. 
    """

    config_location=None

    if configfile: 
        config_location=configfile
    else: 
        config_location = DEFAULT_CONFIG_SOURCEFILE

    # Now parse commandline options (Here??? This code smells bad.)
    parser = argparse.ArgumentParser(
        description="Synchronize events.csv to Google "
            "Calendar",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    parser.add_argument('-c', '--configfile', 
        help='configuration file location',
        default=DEFAULT_CONFIG_SOURCEFILE,
        )
    parser.add_argument('-o', '--operation',
        help='operation to perform',
        default='sync_upcoming',
        choices=['sync-upcoming','sync-all', 'clear']
        )

    args = parser.parse_args()
    if args.configfile:
        config_location = os.path.abspath(args.configfile)

    script_operation = args.operation

    # http://stackoverflow.com/questions/11990556/python-how-to-make-global 
    global config


    # Blargh. You can load modules from paths, but the syntax is
    # different depending on the version of python. 
    # http://stackoverflow.com/questions/67631/how-to-import-a-mod
    # https://stackoverflow.com/questions/1093322/how-do-i-ch

    if sys.version_info >= (3,5): 
        import importlib.util 
        spec = importlib.util.spec_from_file_location(
            'config',
            config_location,
            )
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
    elif sys.version_info >= (3,3):
        # This is the only one I can test. Sad!
        from importlib.machinery import SourceFileLoader
        config = SourceFileLoader( 'config', config_location,).load_module()
    else:
        import imp
        config = imp.load_source( 'config', config_location,)

    # For test harness
    return config
            
# ------------------------------
def load_csv_dicts():
    """ Load CSV files. Yay copy and paste.
    """
    with open(config.EVENTS_CSV, encoding='utf-8-sig') as events_csv:
        reader_events = csv.DictReader(events_csv)

        for row in reader_events:
            # Make a key that will be unique but is easily 
            # sorted by start date.
            new_key = "{}--{}".format(row['DateTimeStart'],
                                      row['RowID'],
                                      )
            events_dict[new_key] = row

    with open(config.POSITIONS_CSV, encoding='utf-8-sig') as positions_csv:
        reader_events = csv.DictReader(positions_csv)

        for row in reader_events:
            positions_dict[row['PositionUniqueName']] = row


# ------------------------------
def connect_to_calendar():
    # From: https://developers.google.com/api-client-library/python/auth/service-accounts
    SCOPES=['https://www.googleapis.com/auth/calendar']

    credentials = service_account.Credentials.from_service_account_file(
        config.SERVICE_CREDENTIALS,
        scopes=SCOPES,
        )

    cal_object = googleapiclient.discovery.build(
        'calendar',
        'v3',
        credentials=credentials,
        )
    return cal_object

# ===== MAIN PROGRAM =======

load_config()

load_csv_dicts()

cal = connect_to_calendar()

# Need to handle exceptions in responses!
# Grab events we know so far. 
existing_events = cal.events().list(
    calendarId=config.CALENDAR_ID,
    orderBy='updated',
    showDeleted='true',).execute()

# Map existing IDs 
existing_ids = {}
for ev in existing_events['items']:
    existing_ids[ev['id']] = True

for k in sorted(events_dict.keys()):
    ev = events_dict[k]

    desc = '<p>Website: <a href="{}">{}</a></p>'.format(
        ev['URL'],
        ev['URL'],
        )
    desc += '<p>{}</p><p>Tags: {}</p>'.format(
        ev['Notes'],
        ev['PositionIDList'],
        )

    bodydict = {
        'start':{
            'dateTime': get_datetime(ev['DateTimeStart']),
            'timeZone': config.TIMEZONE,
            },
        'end':{
            'dateTime': get_datetime(ev['DateTimeEnd']),
            'timeZone': config.TIMEZONE,
            },
        'id': get_padded_id(ev['RowID']),
        'description': desc,
        'location': ev['Location'],
        'source': { 'url' : ev['URL']},
        'summary': ev['Title'],
        }
    
    if ev['CancelledOrRescheduled'] == "Cancelled":
        bodydict['status'] = 'cancelled'

    # If the entry exists then update, else create
    if get_padded_id(ev['RowID']) in existing_ids:
        print("Update: {}".format(ev['Title']))
        event_add = cal.events().update(
            calendarId=config.CALENDAR_ID,
            eventId=get_padded_id(ev['RowID']),
            body=bodydict,
            ).execute()
    else:
        print("Insert: {}".format(ev['Title']))
        event_add = cal.events().insert(
            calendarId=config.CALENDAR_ID,
            body=bodydict,
            ).execute()

    #pprint.pprint(event_add)

     
    # print("{} : {}".format(
    #    k,
    #    events_dict[k]['Title'],
    #    ))

#pprint.pprint(existing_events)
