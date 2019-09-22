#!/usr/bin/env python3

import requests
import tempfile
import filecmp
import sys
import time

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

TARGETDIR='../docs/_data/sync'

COMMIT_NEEDED=False

# Probably I should use a module for this? Or have different
# debug levels? Whatever. 
DEBUG_SCREEN=True
DEBUG_LOG=True 
DEBUG_FILE='/tmp/gdocs-get.log'
DEBUG_FILEHANDLE=None
DEBUG_THRESHOLD=1


# --- Why open here?? ---

if DEBUG_LOG:
    DEBUG_FILEHANDLE = open(DEBUG_FILE, 'w', newline='') 
    # What if this fails?
    if not DEBUG_FILEHANDLE:
        print("Unable to write to {}".format(DEBUG_FILE))
        sys.exit(1)

# --- FUNCTIONS ---

def debug(msg,level=2):
    """ Add debug information to screen and or file. """

    if DEBUG_SCREEN and level <= DEBUG_THRESHOLD:
        print(msg)

    if DEBUG_LOG and level <= DEBUG_THRESHOLD:
        DEBUG_FILEHANDLE.write(msg)

def cleanup():
    """ Clean up file handles. """
    if DEBUG_FILEHANDLE:
        DEBUG_FILEHANDLE.close()

# --- END FUNCTIONS ---

for syncfile in sources:
    debug("file: {}, target: {}".format(
            syncfile,
            sources[syncfile],
            ))
    r = requests.get(sources[syncfile])
     
    # Check that we actually got the file. Otherwise 
    # just continue.

    # https://stackabuse.com/download-files-with-python/
    if r.status_code == 200:
        this_file_different = False

        candidate="{}/{}".format(TMPDIR.name,syncfile)

        with open(candidate, 'wb') as f:
            f.write(r.content)
            f.close()

        origfile="{}/{}".format(TARGETDIR,syncfile)

        if not filecmp.cmp(candidate, origfile):
            this_file_different=True
            debug("Found different files: "
                  "{}. Overwriting.".format(syncfile),
                 1)

            with open(origfile, 'wb') as f_orig:
                f_orig.write(r.content)
                f_orig.close()
        else:
            debug("{}: files are the same")

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


cleanup()
