#!/usr/bin/env python3

import requests
import tempfile
import filecmp
import sys
import time
import datetime
import argparse, sys, os
from git import Repo

""" Grab data files from Google docs
    Paul "Worthless" Nijjar, 2019-09-22
"""

TMPDIR=tempfile.TemporaryDirectory()

DEBUG_DEFAULT_LEVEL=2


# --- Copy and paste ridiculous config code
# See: http://www.karoltomala.com/blog/?p=622
DEFAULT_CONFIG_SOURCEFILE = os.path.join(
    os.getcwd(),
    'gdocs-get-csv.config.py',
    )



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
        description="Synchronize from Google Docs to "
            "local csv files",
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

    if config.DEBUG_DEFAULT_LEVEL:
        DEBUG_DEFAULT_LEVEL = config.DEBUG_DEFAULT_LEVEL

    # For test harness
    return config
            

# --- FUNCTIONS --

def setup_debug_log():
    if config.DEBUG_LOG:
        global DEBUG_FILEHANDLE
        DEBUG_FILEHANDLE = open(config.DEBUG_FILE, 'a', newline='') 
        # What if this fails?
        if not DEBUG_FILEHANDLE:
            print("Unable to write to {}".format(config.DEBUG_FILE))
            sys.exit(1)



def debug(msg,level=DEBUG_DEFAULT_LEVEL):
    """ Add debug information to screen and or file. """

    if config.DEBUG_SCREEN and level <= config.DEBUG_SCREEN_THRESHOLD:
        print(msg)

    if config.DEBUG_LOG and level <= config.DEBUG_LOG_THRESHOLD:
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

load_config()
setup_debug_log()

debug("---- Beginning run ----",1)

changed_files = []

sources = config.SOURCES

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

        origfile="{}/{}/{}".format(
          config.GITDIR,
          config.TARGETDIR,
          syncfile)

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
    repo = Repo(config.GITDIR)
    origin = repo.remote('origin')
    origin.pull()


    commit_msg = "Auto-commit: updated "
    commit_msg += "{} from Google Docs".format( 
                     ", ".join(changed_files))

    debug(commit_msg, 1)

    changed_with_path = map(
      lambda x: "{}/{}".format(config.TARGETDIR, x),
      changed_files)

    repo.index.add(changed_with_path)
    repo.index.commit(commit_msg)
    origin.push()
else:
    debug("All files are the same. Not committing.", 2)

cleanup()
