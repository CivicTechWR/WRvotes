#!/usr/bin/env python3

import requests
from requests_file import FileAdapter
import tempfile
import filecmp
import time
import datetime
import argparse, sys, os, os.path
import pandas
import yaml
import shutil
import argparse

from git import Repo
from sync_poliblog import sync_poliblog

""" Grab data files from NextCloud
    Paul "Worthless" Nijjar, 2022-08-26
"""

TMPDIR=tempfile.TemporaryDirectory()

# Sigh. Should this be global? Probably not.
config = None
args = None


# ------ PARSE ARGS -------
parser = argparse.ArgumentParser(
  description = "Pull WaterlooRegionVotes files from the INTERNET and"
      " convert to csv files"
  )

parser.add_argument("--configfile",
  help = "Where to find the config YAML",
  default = 'get-csv-config.yml',
  )
parser.add_argument("--debuglevel",
  help = "How verbose to be. Higher is more verbose.",
  type = int,
  default = 2,
  )
args = parser.parse_args()

# ---------------------------------
def load_config():
    # From:
    # https://dev.to/jmarhee/using-pyyaml-to-support-yaml-and-json-configuration-files-in-your-cli-tools-1694

    with open(args.configfile, "r") as c:
        cfg = yaml.safe_load(c)
        return cfg


# -----------------------------------
def build_cached_filepath(filename):

    origfile="{}/{}/{}".format(
      config['gitdir'],
      config['targetdir'],
      filename)
    return origfile

# -----------------------------------
def check_changes(filename, candidate, changed_files):
    """ Check if candidate is different than the original
        file. 

        filename: a string
        candidate: a path
        changed_files: an array that gets modified
    """

    origfile=build_cached_filepath(filename)

    if not filecmp.cmp(candidate, origfile):
        debug("Found different files: "
              "{}. Overwriting.".format(filename),
             2)
        shutil.copy(candidate, origfile)
        changed_files.append(filename)

    else:
        debug("{}: files are the same".format(filename),2)


# ------------------------------------
def setup_debug_log():
    # Better hope this is not an error!
    dbg = config['debug']

    if dbg['file']['enable']:
        global DEBUG_FILEHANDLE
        target = dbg['file']['filename']
        DEBUG_FILEHANDLE = open(target, 'a', newline='') 
        # What if this fails?
        if not DEBUG_FILEHANDLE:
            print("Unable to write to {}".format(target))
            sys.exit(1)


# ---------------------------------------
def debug(msg, level):
    """ Add debug information to screen and or file. """

    dbg = config['debug']
    

    if dbg['screen']['enable'] and \
      level <= max(args.debuglevel, dbg['screen']['threshold']):
        print(msg)

    if DEBUG_FILEHANDLE and \
      level <= max(args.debuglevel, dbg['file']['threshold']):
        DEBUG_FILEHANDLE.write("{}: ".format(
          datetime.datetime.now())
          )
        DEBUG_FILEHANDLE.write(msg)
        DEBUG_FILEHANDLE.write('\n')

# ----------------------------------------
def cleanup():
    """ Clean up file handles. """
    if DEBUG_FILEHANDLE:
        DEBUG_FILEHANDLE.close()



# ---- MAIN -------------------

config = load_config()
setup_debug_log()

debug("---- Beginning Run ----", 1)
changed_files = []

# Download source files 
srcdict = {}
destdict = {}

src = config['sources']

req = requests.Session()
req.mount('file://', FileAdapter())
    
for syncfile in config['sources']:
    src = config['sources'][syncfile]
    debug("Fetching {}".format(src), 4)
    debug("src['url']: {}".format(src['url']), 4)
    cached_file = build_cached_filepath(src['localfile'])
    download_success = False

    try:
        r = req.get(src['url'])


        # Check that we actually got the file. Otherwise 
        # just continue.

        # https://stackabuse.com/download-files-with-python/
        if r.status_code == 200:

            candidate="{}/{}".format(
                TMPDIR.name,
                src['localfile'])

            with open(candidate, 'wb') as f:
                f.write(r.content)
                f.close()
            srcdict[syncfile] = candidate

            download_success = True
            
            debug("Saved {} to {}".format(
                src['url'],
                candidate,
                ), 3)
        

            # Fine. Copy source files too.
            if not ('no_copy' in src) or (not src['no_copy']): 
                check_changes(src['localfile'], candidate, changed_files)

        else:
            debug("Oops. Received status "
                  "{} when downloading {} ".format(
                      r.status_code,
                      src['url']
                      ), 0,)



    except (requests.Timeout, requests.ConnectionError) as e:
        debug("Failed to fetch {}. Error: {}".format(src['url'], e), 0)
        

    if not download_success:
        if os.path.isfile(cached_file):
            debug("Using {} as cached version instead".format(
              cached_file
              ),0)
            srcdict[syncfile] = cached_file
        else:
            debug("Oops. No cached file available."
                  " I guess we crash?",
                  0)

debug("srcdict is {}".format(srcdict),4)

# For :each destination
for syncdest in config['dests']:
    dest = config['dests'][syncdest]

    candidate="{}/{}".format(
        TMPDIR.name,
        syncdest)

    # This will crash if the read failed, which is fine.
    # No it is not fine. 
    src = srcdict[dest['source']]
    
    if dest['format'] == 'ods':
        df = pandas.read_excel(
            src,
            engine='odf',
            sheet_name=dest['sheet'],
            )
        df.to_csv(candidate, index=None, header=True)
        destdict[syncdest] = candidate

        
        debug("Saved {} to {}".format(
            syncdest,
            candidate,
            ),3)

    elif dest['format'] == 'csv':
        shutil.copy(src, candidate)
        destdict[syncdest] = candidate

    else: 
        debug("Oops. Unknown format {} for {}".format(
            dest['format'], 
            'syncdest'
            ),0)

    # Don't compare all files
    if not ('no_copy' in dest) or (not dest['no_copy']): 
        check_changes(syncdest, candidate, changed_files)


if config['merge_poliblog']: 
    new_nominees="{}/{}".format(TMPDIR.name, config['nominees'],)
    sync_poliblog(
        destdict['poliblog.csv'],
        destdict['overrides.csv'],
        new_nominees,
        )

    check_changes(
        config['nominees'], 
        new_nominees, 
        changed_files,
        )

# Check in

debug("changed_files is {}".format(changed_files),3)
if changed_files:
    repo = Repo(config['gitdir'])
    origin = repo.remote('origin')

    origin.pull()


    commit_msg = "Auto-commit: updated "
    commit_msg += "{} from web editor".format( 
                     ", ".join(changed_files))

    debug(commit_msg, 2)

    changed_with_path = map(
      lambda x: "{}/{}".format(config['targetdir'], x),
      changed_files)

    repo.index.add(changed_with_path)
    repo.index.commit(commit_msg)
    origin.push()
else:
    debug("All files are the same. Not committing.", 2)

cleanup()
