#!/usr/bin/env python3
"""
Compare Poliblog CSV against our own. Report differences.

Paul "Worthless" Nijjar, 2026-08-11
"""

import unicodedata
import yaml
import argparse, sys, os
import dateutil.parser, pytz, datetime
import csv


# Data is in a dict 
d = {}
errors = []

in_poliblog_only = []
in_ours_only = []

i_set_debug_filehandle = False

DEBUG_DEFAULT_LEVEL = 2

# ------ PARSE ARGS -------
def parse_args():
    parser = argparse.ArgumentParser(
      description = "Analyse difference from Poliblog CSV"
      )

    parser.add_argument("--configfile",
      help = "Where to find the config YAML",
      required = True,
      )
    parser.add_argument("--debuglevel",
      help = "How verbose to be. Higher is more verbose.",
      type = int,
      default = 2,
      )
    parser.add_argument("--poliblog-csv",
      help = "Path to poliblog CSV file",
      required = True,
      )
    parser.add_argument("--wrv-csv",
      help = "Path to waterlooregionvotes nominee CSV file",
      required = True,
      )
    parser.add_argument("--tests",
      choices=['wrv_candidate_missing', 'wrv_socialmedia_missing',
        'poliblog_candidate_missing', 'poliblog_socialmedia_missing',
        'socialmedia_conflict'],
      default=['wrv_candidate_missing', 'wrv_socialmedia_missing',],
      )
    return parser.parse_args()

# ---------------------------------
def load_config(args):
    # From:
    # https://dev.to/jmarhee/using-pyyaml-to-support-yaml-and-json-configuration-files-in-your-cli-tools-1694

    with open(args.configfile, "r") as c:
        cfg = yaml.safe_load(c)
        cfg.update(vars(args))
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


# ------------------
def print_header(msg, level): 
    """ Make a header for the report that does not look stupid
      (just kidding it looks stupid)
    """

    debug("-----------------------------",level)
    debug(msg, level)
    debug("-----------------------------\n",level)


# -------------------
def find_missing_candidates(lookup_src, target_src):
    """ Identify missing candidates in target_src that are in
    lookup_src

    """
    print_header("Candidates present in {} but missing from {}".format(
      lookup_src,
      target_src,
      ), 
      1)
    

    for row_key in d[lookup_src]:
        if not row_key in d[target_src]:
            
            errmsg = "Candidate {} is in {} but is missing from {}".format(
                row_key,
                lookup_src,
                target_src,
                )

            if lookup_src == 'poliblog':
                if d[lookup_src][row_key]['Not_Running']:
                    # No problem here. 
                    continue
                if d[lookup_src][row_key]['Incumbent']:
                    errmsg = "Candidate {} is missing but may be an " \
                             "incumbent: {}. Found in {} but " \
                             "not {}".format(
                        row_key,
                        d[lookup_src][row_key]['Incumbent'],
                        lookup_src,
                        target_src,
                        )
                 

            err(target_src,
              errmsg,
              d[lookup_src][row_key])


# -----------------
def reverse_csv_map(): 
    """ Reverse csv map and return it.
    """

    orig_map = config['csv_map']
    rev_map = {}

    for k in orig_map:
        rev_map[orig_map[k]] = k

    return rev_map

# ------------------
def find_missing_socialmedia(lookup_src, target_src):
    """
    For candidates that exist in both lookup_src and target_src,
    print the missing social media from target_src that is present 
    in lookup_src
    """


    print_header("Social media present in {} but missing from {}".format(
      lookup_src,
      target_src,
      ), 
      1)

    if lookup_src == 'wrv':
        headermap = config['csv_map']
    elif lookup_src == 'poliblog':
        headermap = reverse_csv_map()


    for row_key in d[lookup_src]:
        if row_key in d[target_src]:
            for media in headermap:
                if d[lookup_src][row_key][media] and  \
                  not d[target_src][row_key][headermap[media]]:

                    debug("{}: missing social media {}: {}".
                      format(
                        row_key,
                        headermap[media],
                        d[lookup_src][row_key][media],
                        ), 1)
            

# ------------------
def find_conflicting_socialmedia(lookup_src, target_src):
    """
    For candidates that exist in both lookup_src and target_src,
    print the social media that conflicts between the two  
    """


    print_header("Conflicting social media listings", 1)

    if lookup_src == 'wrv':
        headermap = config['csv_map']
    elif lookup_src == 'poliblog':
        headermap = reverse_csv_map()


    for row_key in d[lookup_src]:
        if row_key in d[target_src]:
            for media in headermap:
                if d[lookup_src][row_key][media] and  \
                   d[target_src][row_key][headermap[media]] and \
                   not (d[lookup_src][row_key][media] ==
                     d[target_src][row_key][headermap[media]]):

                    debug("{}: CONFLICT  social media for {}: "
                      "{} : {} and {} : {}".
                      format(
                        row_key,
                        headermap[media],
                        lookup_src,
                        d[lookup_src][row_key][media],
                        target_src,
                        d[target_src][row_key][headermap[media]],
                        ), 1)
            


# -------------------
def get_key_id(sourcetype, row):
    """ Given a row and the source type, generate the unique key. """
    if sourcetype == 'poliblog':
        return row['Name']
    elif sourcetype == 'wrv':
        return "{} {}".format(row['Given_Names'], row['Last_Name'])

# --------------------
def run_checker(cfg, dbg_filehandle = None):
    """ Load CSV files and launch checker"""

    global config
    config = cfg

    debug("Config is {}".format(cfg), 5)

    if not dbg_filehandle: 
        setup_debug_log()
    else:
        global DEBUG_FILEHANDLE
        DEBUG_FILEHANDLE = dbg_filehandle

    for csv_src in [config['poliblog_csv'], config['wrv_csv']]:
        debug("Opening {}".format(csv_src))

        sourcetype = 'wrv'
        if csv_src == config['poliblog_csv']:
            sourcetype = 'poliblog'
            
        
        with open (csv_src, encoding='utf-8') as f:
            # Skip first line of poliblog
            if sourcetype == 'poliblog':
                f.readline()

            reader = csv.DictReader(f)
            d[sourcetype] = {}

            for row in reader: 
                key_id = get_key_id(sourcetype, row)
                if not key_id:
                    debug("{}: No key found in {}".format(
                      sourcetype,
                      row,), 5)
                    continue
                elif key_id in d[sourcetype]:
                    if sourcetype == 'poliblog' and \
                        row['Not_Running']:

                        # Bob puts multiple entries if a candidate
                        # is leaving one office to go to another

                        debug("{}: Skipped {} because '{}'".format(
                          sourcetype,
                          key_id,
                          row['Not_Running'],
                          ), 3)

                    elif sourcetype == 'poliblog' and \
                      d[sourcetype][key_id]['Not_Running']:

                        debug("{}: Overwrote {}: orig was '{}'".format(
                          sourcetype,
                          key_id,
                          d[sourcetype][key_id]['Not_Running'],
                          ), 3)

                        d[sourcetype][key_id] = row

                    else:
                        err(
                          sourcetype,
                          "{}: Duplicate key {}".format(
                            sourcetype,
                            key_id,
                            ),
                            row)
                        continue
                      
                d[sourcetype][key_id]= row
                

        debug("{}: Read {} records".format(
          sourcetype,
          len(d[sourcetype]),
          ), 4)

    debug("{} is {}".format(
      'wrv',
      d['wrv'],
      ), 6)


    if 'poliblog_candidate_missing' in config['tests']: 
        find_missing_candidates('wrv','poliblog')

    if 'poliblog_socialmedia_missing' in config['tests']: 
        find_missing_socialmedia('wrv','poliblog')

    if 'wrv_candidate_missing' in config['tests']: 
        find_missing_candidates('poliblog','wrv')

    if 'wrv_socialmedia_missing' in config['tests']: 
        find_missing_socialmedia('poliblog','wrv')

    if 'socialmedia_conflict' in config['tests']: 
        find_conflicting_socialmedia('poliblog','wrv')



    num_errors = len(errors)
    if num_errors > 0:
        debug("TOTAL: Found {} errors".format(num_errors),0)

# --------------------
# --------------------
# --------------------
# --- END FUNCTIONS ---

if __name__ == "__main__":
    args = parse_args()
    cfg = load_config(args)
    run_checker(cfg)
    cleanup()
    



