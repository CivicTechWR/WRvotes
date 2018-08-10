#!/usr/bin/env python3
"""
Take events.csv and put it into a Google calendar, using 
patching to update event info. 

Paul "Worthless" Nijjar, 2018-08-08
"""

import csv, json
import argparse, sys, os
import pprint
import dateutil.parser, pytz, datetime
from google.oauth2 import service_account
import googleapiclient.discovery


# '/home/pnijjar/watcamp/python_rss/gcal_helpers/config.py'
# See: http://www.karoltomala.com/blog/?p=622
DEFAULT_CONFIG_SOURCEFILE = os.path.join(
    os.getcwd(),
    'update-google-calendar.config.py',
    )


INVALID_DATE = datetime.datetime(1969,12,12,
    tzinfo=pytz.timezone('UTC'))

events_dict = {}
positions_dict = {}

# ------------------------------
def get_today():
    """ Gets current time as of midnight."""

    target_timezone = pytz.timezone(config.TIMEZONE)
    today = datetime.datetime.now(tz=target_timezone)

    today = today.replace(hour=0, minute=0, second=0)

    return today

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
        default='sync-upcoming',
        choices=['sync-upcoming','sync-all']
        )

    args = parser.parse_args()
    if args.configfile:
        config_location = os.path.abspath(args.configfile)

    global script_operation
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


# ------------------------------
def sync_calendar(cal, include_all=False):
    """ Synchronize the events.csv to the Google calendar.
    """

    load_csv_dicts()

    since_when = get_today()

    if include_all:
        since_when = INVALID_DATE

    # Format looks like: 2017-03-25T00:00:00-0500
    since_when_formatted = since_when.strftime("%Y-%m-%dT%H:%M:%S%z")

    # Grab events we know so far. 
    existing_events = cal.events().list(
        calendarId=config.CALENDAR_ID,
        orderBy='updated',
        singleEvents='true',
        showDeleted='true',
        timeMin = since_when_formatted,
        ).execute()

    # Map existing IDs 
    existing_ids = {}
    for ev in existing_events['items']:
        existing_ids[ev['id']] = True

    for k in sorted(events_dict.keys()):
        ev = events_dict[k]

        datetime_end = dateutil.parser.parse(ev['DateTimeEnd'])
        # Make date timezone-aware (sigh)
        tz = pytz.timezone(config.TIMEZONE)
        datetime_end = tz.localize(datetime_end)

        # If the event is in the past, then 
        if datetime_end < since_when:
            # print("IGNORED: {}".format(ev['Title']))
            continue
           
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
            # print("Update: {}".format(ev['Title']))
            event_add = cal.events().update(
                calendarId=config.CALENDAR_ID,
                eventId=get_padded_id(ev['RowID']),
                body=bodydict,
                ).execute()
        else:
            # print("Insert: {}".format(ev['Title']))
            event_add = cal.events().insert(
                calendarId=config.CALENDAR_ID,
                body=bodydict,
                ).execute()

    #pprint.pprint(existing_events)



# ===== MAIN PROGRAM =======

load_config()
cal = connect_to_calendar()

#print("Main: script_operation: {}".format(script_operation))

if script_operation == 'sync-upcoming':
    sync_calendar(cal)
elif script_operation == 'sync-all':
    sync_calendar(cal, True)
else:
    print("Unknown operation: {}".format(script_operation))
