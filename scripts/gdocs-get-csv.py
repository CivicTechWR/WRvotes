#!/usr/bin/env python3

import requests
import tempfile
import filecmp
import sys
import time
import datetime
from git import Repo

""" Grab data files from Google docs
    Paul "Worthless" Nijjar, 2019-09-22
"""

### --- Sources ---

# format: localfile: remotesource
sources = {
  'nominees.csv': 'https://docs.google.com/spreadsheets/d/1rsQksqAJjyVzjs9pA49dRij-fC-hwG8nORMmlTx_9_I/export?format=csv&id=1rsQksqAJjyVzjs9pA49dRij-fC-hwG8nORMmlTx_9_I&gid=917247882',
  'events.csv': 'https://docs.google.com/spreadsheets/d/1sIfYfey7D72Uyi1NOAxrAFbU6yn9HvIUjINCqYGHwMw/export?format=csv&id=1sIfYfey7D72Uyi1NOAxrAFbU6yn9HvIUjINCqYGHwMw&gid=103989638',
  'media.csv': 'https://docs.google.com/spreadsheets/d/1sIfYfey7D72Uyi1NOAxrAFbU6yn9HvIUjINCqYGHwMw/export?format=csv&id=1sIfYfey7D72Uyi1NOAxrAFbU6yn9HvIUjINCqYGHwMw&gid=1989058875',
  }

TMPDIR=tempfile.TemporaryDirectory()

GITDIR='/home/pnijjar/src/wrvotesfed-pnijjar'
TARGETDIR="docs/_data/sync"

# Probably I should use a module for this? Whatever.
DEBUG_SCREEN=True
DEBUG_LOG=True 
DEBUG_FILE='/tmp/gdocs-get.log'
DEBUG_FILEHANDLE=None
DEBUG_LOG_THRESHOLD=1
DEBUG_SCREEN_THRESHOLD=0
DEBUG_DEFAULT_LEVEL=3

# --- Why open here?? ---

if DEBUG_LOG:
    DEBUG_FILEHANDLE = open(DEBUG_FILE, 'a', newline='') 
    # What if this fails?
    if not DEBUG_FILEHANDLE:
        print("Unable to write to {}".format(DEBUG_FILE))
        sys.exit(1)

# --- FUNCTIONS ---

def debug(msg,level=DEBUG_DEFAULT_LEVEL):
    """ Add debug information to screen and or file. """

    if DEBUG_SCREEN and level <= DEBUG_SCREEN_THRESHOLD:
        print(msg)

    if DEBUG_LOG and level <= DEBUG_LOG_THRESHOLD:
        DEBUG_FILEHANDLE.write("{}: ".format(
          datetime.datetime.now())
          )
        DEBUG_FILEHANDLE.write(msg)
        DEBUG_FILEHANDLE.write('\n')

def cleanup():
    """ Clean up file handles. """
    if DEBUG_FILEHANDLE:
        DEBUG_FILEHANDLE.close()

# --- END FUNCTIONS ---

debug("---- Beginning run ----",1)

changed_files = []

for syncfile in sources:
    debug("file: {}, target: {}".format(
            syncfile,
            sources[syncfile],
            ),
            3)
    r = requests.get(sources[syncfile])
     
    # Check that we actually got the file. Otherwise 
    # just continue.

    # https://stackabuse.com/download-files-with-python/
    if r.status_code == 200:

        candidate="{}/{}".format(TMPDIR.name,syncfile)

        with open(candidate, 'wb') as f:
            f.write(r.content)
            f.close()

        origfile="{}/{}/{}".format(GITDIR,TARGETDIR,syncfile)

        if not filecmp.cmp(candidate, origfile):
            debug("Found different files: "
                  "{}. Overwriting.".format(syncfile),
                 2)
            changed_files.append(syncfile)

            with open(origfile, 'wb') as f_orig:
                f_orig.write(r.content)
                f_orig.close()
        else:
            debug("{}: files are the same".format(syncfile),2)

    else:
        debug("Oops. Received status "
              "{} when downloading {} "
               "from {} .".format(
                  r.status_code,
                  syncfile,
                  sources[syncfile]
                  ),
             0,
             )

if changed_files:
    repo = Repo(GITDIR)


    commit_msg = "Auto-commit: updated "
    commit_msg += "{} from Google Docs".format( 
                     ", ".join(changed_files))

    debug(commit_msg, 1)

    changed_with_path = map(
      lambda x: "{}/{}".format(TARGETDIR, x),
      changed_files)

    repo.index.add(changed_with_path)
    repo.index.commit(commit_msg)
    origin = repo.remote('origin')
    origin.push()
else:
    debug("All files are the same. Not committing.", 2)

cleanup()
