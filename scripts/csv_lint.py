#!/usr/bin/env python3
"""
Check CSV files for errors, and throw an error with details if
applicable.

Paul "Worthless" Nijjar, 2026-06-05
"""

import csv, re
import unicodedata
import yaml
import argparse, sys, os
import dateutil.parser, pytz, datetime


# Data is in a dict 
d = {}
errors = []

i_set_debug_filehandle = False

DEBUG_DEFAULT_LEVEL = 2

# ------ PARSE ARGS -------
def parse_args_linter():
    parser = argparse.ArgumentParser(
      description = "Analyse CSV files for errors"
      )

    parser.add_argument("--configfile",
      help = "Where to find the config YAML",
      required = True,
      )
    parser.add_argument("--debuglevel",
      help = "How verbose to be. Higher is more verbose.",
      type = int,
      )
    return parser.parse_args()

# ---------------------------------
def load_config(args):
    # From:
    # https://dev.to/jmarhee/using-pyyaml-to-support-yaml-and-json-configuration-files-in-your-cli-tools-1694

    with open(args.configfile, "r") as c:
        cfg = yaml.safe_load(c)
        return cfg


# ------------------------------------
def setup_debug_log():
    # Better hope this is not an error!
    dbg = config['debug']

    if dbg['log']['enable']:
        global DEBUG_FILEHANDLE
        target = dbg['log']['logfile']
        DEBUG_FILEHANDLE = open(target, 'a', newline='') 
        # What if this fails?
        if not DEBUG_FILEHANDLE:
            print("Unable to write to {}".format(target))
            sys.exit(1)

    if 'level' in dbg['default']:
        DEBUG_DEFAULT_LEVEL = dbg['default']['level']

    if config['debuglevel']:
        dbg['screen']['threshold'] = config['debuglevel']
        dbg['log']['threshold'] = config['debuglevel']

    i_set_debug_filehandle = True

# --------------------
def debug(msg,level=DEBUG_DEFAULT_LEVEL):
    """ Add debug information to screen and or file. """

    if config['debug']['screen']['enable'] and \
      level <= config['debug']['screen']['threshold']:
        print(msg)

    if config['debug']['log']['enable'] and \
      level <= config['debug']['log']['threshold']:
        DEBUG_FILEHANDLE.write("{}: ".format(
          datetime.datetime.now())
          )
        DEBUG_FILEHANDLE.write(msg)
        DEBUG_FILEHANDLE.write('\n')


# --------------------
def err(sourcefile, msg, record):
   """ Register incorrect info """

   compile_str = "{}: {}\n\trecord: {}".format(
     sourcefile,
     msg,
     record)

   errors.append(compile_str)
   debug(compile_str + "\n", config['debug']['errors']['level'])

   
# --------------------
def cleanup():
    """ Clean up file handles. """
    if DEBUG_FILEHANDLE and i_set_debug_filehandle:
        DEBUG_FILEHANDLE.close()


# -------------------------------
def get_localized_datetime_obj(
  datetime_str, 
  source_csv='events',
  record=None
  ):
   """ Get a localized datetime object from a string. 
       This is different than get_datetime because it does 
       not produce a string.
   """
   d = dateutil.parser.parse(datetime_str)
   # Make date timezone-aware (sigh)
   try:
       tz = pytz.timezone(config['timezone'])
       d = tz.localize(d)
   except ValueError:
       # Huh. I guess I need another?
       err(source_csv, "ERROR: already localized: {}".format(d), record)

   return d


# --------------------
def check_nominees():

    for nom_id in d['nominees']:
        nominee = d['nominees'][nom_id]

        # Nominee should unique UniqueID (checked when reading CSV)
    
        # Nominee should have first and last name?

        # Nominee position should be valid
        position = nominee['PositionUniqueName']
        if not position in d['position-tags']:
            err('nominees',
              "Candidate {} {} with ID {} is running for position {}, which does"
              " not exist".format(
                nominee['Given_Names'],
                nominee['Last_Name'],
                nominee['UniqueID'],
                position,
                ),
              nominee,
              )
        elif int(d['position-tags'][position]['NumberToElect']) == 0:
            err('nominees',
              "Candidate {} {} with ID {} is running for position {}, which "
              "is supposed to elect 0 candidates and is probably not a "
              "real position!".format(
                nominee['Given_Names'],
                nominee['Last_Name'],
                nominee['UniqueID'],
                position,
                ),
              nominee,
              )
         
    
    

# --------------------
def check_media():

    # Nothing could possibly go wrong with this.
    date_format = re.compile(r'^\d\d\d\d-\d\d-\d\d$')


    for media_id in d['media']:
        m = d['media'][media_id]

        # PubDate should be present and a date. Ugh regex.
        if not date_format.match(m['PubDate']):
            err('media',
              "Media item has date '{}', which does not appear to be "
              "in ISO format: YYYY-MM-DD. (Check the dashes if everything else "
              "seems right.))".format(m['PubDate']),
              m)

        # Title should exist
        if m['Title'] == '':
            err('media', "Item does not appear to have title", m)

        # Publication should exist
        if m['Publication'] == '':
            err('media', "Item does not appear to have publication", m)

        # PositionIDList should exist (?) and every position should be
        # valid
        check_position_id_list(m['PositionIDList'], 'media', m)

        # Category should exist and be valid (and there should be just
        # 1?)
        category = m['Category']
        if category == '':
            err('media', 'Item does not appear to have a category',m)

        elif category not in d['media-categories']:
            err('media',
              "Item has category '{}', which does not "
              "appear to be a category in media-categories.csv".format(
                category,
                ),
              m)


        # SubCategory should be valid if it exists


# --------------------
def check_events():
    for event_id in d['events']:
        ev = d['events'][event_id]

        start_datetime_exists = False
        end_datetime_exists = False

        # Event should have start date and time
        if ev['DateTimeStart'] == '':
            err('events', 
              "Event does not appear to have a start date/time", 
              ev)
        else:
            start_datetime_exists = True

        # Event should have end date and time
        if ev['DateTimeEnd'] == '':
            err('events', 
              "Event does not appear to have an end date/time", 
              ev)
        else:
            end_datetime_exists = True


        if start_datetime_exists and end_datetime_exists:
            try:
                start_datetime = get_localized_datetime_obj(
                  ev['DateTimeStart'],
                  'events',
                  ev)

                end_datetime = get_localized_datetime_obj(
                  ev['DateTimeEnd'],
                  'events',
                  ev)

                # End should be after start
                if end_datetime < start_datetime:
                    err('events',
                      "End date/time {} appears to be before "
                      "start date/time {}".format(
                        end_datetime,
                        start_datetime,
                        ),
                      ev)

            except Exception as e:
                err('events', "{}".format(e), ev)

        # Title should exist
        if ev['Title'] == '':
            err('events',
              "Event does not appear to have a title",
              ev)

        # PositionIDLists should be valid
        check_position_id_list(ev['PositionIDList'], 'events', ev)

        # Location should not be empty (use "online" for virtual
        # events)
        if ev['Location'] == '':
            err('events',
              "Event does not appear to have a location. "
              "Use 'Online' for virtual events.",
              ev)
  
# --------------------
def check_position_id_list(plist, source_csv, record):
    if plist == '':
        err(source_csv, 
          "Item appears to have no positions listed in PositionIDList",
          record)

    else: 
        position_list = plist.split(',')
        for p_raw in position_list:
            p = p_raw.strip(' ')
            if p not in d['position-tags'] and p not in d['aliases']:
                err(source_csv,
                  "Item has PositionIDTag '{}', which does "
                  "not appear to be in either position-tags.csv "
                  "or aliases.csv".format(p),
                  record)


# --------------------
def run_linter(cfg, dbg_filehandle = None):
    """ Load CSV files and launch linter"""

    global config
    config = cfg

    if not dbg_filehandle: 
        setup_debug_log()
    else:
        global DEBUG_FILEHANDLE
        DEBUG_FILEHANDLE = dbg_filehandle

    for csv_src in config['sources']:
       filepath = os.path.join(
         config['gitdir'],
         config['targetdir'],
         config['sources'][csv_src]['folder'],
         "{}.{}".format(csv_src, 'csv'),
         )

       debug("Filepath for {} is {}".format(
         csv_src,
         filepath,
         ), 4)

       d[csv_src] = {}

       with open (filepath, encoding='utf-8') as f:
           reader = csv.DictReader(f)
           key_id = config['sources'][csv_src]['key']


           for row in reader:
               if not key_id in row or row[key_id] == '':
                   err(
                     csv_src,
                     "Missing unique key '{}'".format(key_id),
                     row,
                     )
                   continue

               if row[key_id] in d[csv_src]:
                   err(
                     csv_src, 
                     "Duplicate key {}".format(row[key_id]),
                     row,
                     )
               d[csv_src][row[key_id]] = row

       debug("{}: Read {} records".format(
         csv_src,
         len(d[csv_src]),
         ), 3)
       
    check_nominees()
    check_media()
    check_events()

    num_errors = len(errors)
    if num_errors > 0:
        debug("TOTAL: Found {} errors".format(num_errors),0)

# --------------------
# --------------------
# --------------------
# --- END FUNCTIONS ---

if __name__ == "__main__":
    args = parse_args_linter()
    cfg = load_config(args)
    run_linter(cfg)
    cleanup()
    



