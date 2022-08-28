#!/usr/bin/env python3

import requests
from requests_file import FileAdapter
import tempfile
import filecmp
import time
import datetime
import argparse, sys, os
import pandas
import yaml
import shutil

from git import Repo
from sync_poliblog import sync_poliblog

""" Grab data files from NextCloud
    Paul "Worthless" Nijjar, 2022-08-26
"""

TMPDIR=tempfile.TemporaryDirectory()

DEBUG_DEFAULT_LEVEL=2
CONFIG_DEFAULT='get-csv-config.yml'
NOMINEES='nominees.csv'

# Sigh. Should this be global? Probably not.
config = None


# ---------------------------------
def load_config(configfile=CONFIG_DEFAULT):
    # From:
    # https://dev.to/jmarhee/using-pyyaml-to-support-yaml-and-json-configuration-files-in-your-cli-tools-1694

    with open(configfile, "r") as c:
        cfg = yaml.safe_load(c)
        return cfg


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
def debug(msg,level=DEBUG_DEFAULT_LEVEL):
    """ Add debug information to screen and or file. """

    dbg = config['debug']

    if dbg['screen']['enable'] and level <= dbg['screen']['threshold']:
        print(msg)

    if DEBUG_FILEHANDLE and level <= dbg['file']['threshold']:
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
        
        debug("Saved {} to {}".format(
            src['url'],
            candidate,
            ),0)
    
    else:
        debug("Oops. Received status "
              "{} when downloading {} ".format(
                  r.status_code,
                  src['url']
                  ),
             0,
             )

debug("srcdict is {}".format(srcdict),4)

# For :each destination
for syncdest in config['dests']:
    dest = config['dests'][syncdest]

    candidate="{}/{}".format(
        TMPDIR.name,
        syncdest)

    # This will crash if the read failed, which is fine.
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
            ),0)

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
        origfile="{}/{}/{}".format(
          config['gitdir'],
          config['targetdir'],
          syncdest)

        if not filecmp.cmp(candidate, origfile):
            debug("Found different files: "
                  "{}. Overwriting.".format(syncdest),
                 0)
            shutil.copy(candidate, origfile)
            changed_files.append(syncdest)

        else:
            debug("{}: files are the same".format(syncdest),0)



# TODO: Merge poliblog
if config['merge_poliblog']: 
    new_nominees="{}/{}".format(TMPDIR.name, NOMINEES,)
    orig_nominees="{}/{}/{}".format(
          config['gitdir'],
          config['targetdir'],
          NOMINEES)

    sync_poliblog(
        destdict['poliblog.csv'],
        destdict['overrides.csv'],
        new_nominees,
        )

    # Ugh this should be a factored out helper function.
    if not filecmp.cmp(new_nominees, orig_nominees):
        debug("Found different files: "
              "{}. Overwriting.".format(NOMINEES))
        shutil.copy(new_nominees, orig_nominees)
        changed_files.append(NOMINEES)



# Check in

debug("changed_files is {}".format(changed_files),0)
if changed_files:
    repo = Repo(config['gitdir'])
    origin = repo.remote('origin')

    origin.pull()


    commit_msg = "Auto-commit: updated "
    commit_msg += "{} from web editor".format( 
                     ", ".join(changed_files))

    debug(commit_msg, 1)

    changed_with_path = map(
      lambda x: "{}/{}".format(config['targetdir'], x),
      changed_files)

    repo.index.add(changed_with_path)
    repo.index.commit(commit_msg)
    origin.push()
else:
    debug("All files are the same. Not committing.", 2)

   

cleanup()
