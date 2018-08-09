#!/usr/bin/env python3
"""
Take events.csv and put it into a Google calendar, using 
patching to update event info. 

Paul "Worthless" Nijjar, 2018-08-08
"""

import csv, json
import argparse, sys, os
import requests

# '/home/pnijjar/watcamp/python_rss/gcal_helpers/config.py'
# See: http://www.karoltomala.com/blog/?p=622
DEFAULT_CONFIG_SOURCEFILE = os.path.join(
    os.getcwd(),
    'update-google-calendar.config.py',
    )

events_dict = {}

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

    args = parser.parse_args()
    if args.configfile:
        config_location = os.path.abspath(args.configfile)

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
            

# ===== MAIN PROGRAM =======

load_config()

# ---- Get credentials -----
with open(config.SERVICE_CREDENTIALS) as f:
    calendar_bot = json.load(f)

print("Email is {}".format(calendar_bot['client_email']))

# ---- Load Events ----
with open(config.EVENTS_CSV, encoding='utf-8-sig') as events_csv:
    reader_events = csv.DictReader(events_csv)

    for row in reader_events:
        events_dict[row['RowID']] = row
        print(row['Title'], row['RowID'])
 
