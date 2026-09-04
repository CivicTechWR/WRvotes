#!/usr/bin/env python3

import requests
import tempfile
import filecmp
import sys
import time
import datetime
import argparse, sys, os
import shutil
import yaml
from git import Repo
from google.oauth2 import service_account
from googleapiclient.discovery import build
import googleapiclient.errors
from googleapiclient.http import MediaIoBaseDownload
import io
import csv_lint

""" Grab data files from Google docs
    Paul "Worthless" Nijjar, 2019-09-22
"""

TMPDIR=tempfile.TemporaryDirectory()
DEBUG_DEFAULT_LEVEL = 2


# ------ PARSE ARGS -------
def parse_args():
    parser = argparse.ArgumentParser(
      description = "Pull WaterlooRegionVotes files from the INTERNET and"
          " convert (some of them) to csv files"
      )

    parser.add_argument("--configfile",
      help = "Where to find the config YAML",
      required = True,
      )
    parser.add_argument("--debuglevel",
      help = "How verbose to be. Higher is more verbose.",
      type = int,
      )
    parser.add_argument("--no-download",
      help = "Do not download CSVs from Google Docs",
      action = "store_true",
      )
    parser.add_argument("--no-lint",
      help = "Do not check CSV files for errors",
      action = "store_true",
      )
    parser.add_argument("--no-commit",
      help = "Do not check files into git and push them",
      action = "store_true",
      )
    return parser.parse_args()

# ---------------------------------
def load_config(args):
    # From:
    # https://dev.to/jmarhee/using-pyyaml-to-support-yaml-and-json-configuration-files-in-your-cli-tools-1694

    with open(args.configfile, "r") as c:
        cfg = yaml.safe_load(c)

        # I want the flags to be in config[]
        cfg.update(vars(args))
        return cfg


# ------------------------------
def auth_to_google():
    # From: https://developers.google.com/api-client-library/python/auth/service-accounts
    SCOPES= [
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/drive.metadata.readonly',
      'https://www.googleapis.com/auth/drive.readonly',
      ]

    credentials = service_account.Credentials.from_service_account_file(
        config['service_credentials'],
        scopes=SCOPES,
        )

    # cal_object = googleapiclient.http.build_http()
    return credentials


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
        config['debug']['screen']['threshold'] = config['debuglevel']
        config['debug']['log']['threshold'] = config['debuglevel']


# ------------------------------------
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

# ------------------------------------
def sync_folders():
    creds = auth_to_google()

    changed_files = []
    committed_changes = False

    sources = config['foldersync']

    for folder in sources:
        localfolder = os.path.join(
          config['gitdir'],
          sources[folder]['localfolder'],
          )
        # Ensure local folder exists
        if not (os.path.isdir(localfolder)):
            debug(
              "{}: local folder {} does not exist."
              "Skipping".format(
                folder,
                localfolder,
                ), 0)
            continue
      
        # Connect to Google Drive
        # Plagiarized from 
        # https://www.pythontutorials.net/blog/list-of-files-in-a-google-drive-folder-with-python/

        try: 
            service = build("drive", "v3", credentials=creds)

            page_token = 'fake-value'
            all_files = []

            while page_token:

                # List files
                results = service.files().list(
                  q="'{}' in parents".format(sources[folder]['remoteid']),
                  fields="nextPageToken, files(id, name)",
                  pageSize=100,
                  ).execute()

                page_token = results.get('nextPageToken')

                filelist = results.get("files", [])
                all_files.extend(filelist)


            debug("sync_folders: got {} files for ID {}".format(
              len(all_files),
              sources[folder]['remoteid'],
              ), 3)

        except googleapiclient.errors.HttpError:
            debug("sync_folders:  exception:\n{}".format(e), 0)
            

        # Download each file to a cached folder.
        # Plagiarized from: https://stackoverflow.com/a/63568558
        with tempfile.TemporaryDirectory() as cachedir:
            for src in all_files:
                cached_target = os.path.join(cachedir, src['name'])
                local_target = os.path.join(localfolder, src['name'])

                try:
                    drivefile = service.files().get_media(fileId=src['id'])

                    f = io.FileIO(cached_target, 'wb')
                    downloader = MediaIoBaseDownload(f, drivefile)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()

                except Exception as e:
                    debug("sync_folders: {} failed with exception {}".format(
                      cached_target,
                      e), 0)

                # If files are different or local_target is missing,
                # then we want to add this to the changed_files to submit
                if os.path.isfile(local_target):

                    if not filecmp.cmp(cached_target, local_target):
                        debug("Found different files: "
                              "{}. Overwriting.".format(local_target),
                             2)
                        changed_files.append(local_target)

                    else:
                        debug("{}: files are the same".format(local_target),3)

                else:
                    # File does not exist. Copy it and add to files to
                    # change.
                    shutil.copy2(cached_target, local_target)
                    debug("New file: {}".format(local_target), 2)
                    changed_files.append(local_target)

        if changed_files:
            return commit_files(changed_files)
            return False
        else:
            debug("No changes to sync. Not committing.", 2)
            return False
            

# ------------------------------------
def download_csvs():
    creds = auth_to_google()


    changed_files = []
    committed_changes = False

    sources = config['sources']

    for syncfile in sources:
        if 'remotesrc' in sources[syncfile]:
            debug("file: {}, target: {}".format(
                    syncfile,
                    sources[syncfile]['remotesrc'],
                    ),
                    3)
            r = requests.get(sources[syncfile]['remotesrc'])
             
            # Check that we actually got the file. Otherwise 
            # just continue.

            # https://stackabuse.com/download-files-with-python/
            if r.status_code == 200:

                candidate="{}/{}.csv".format(TMPDIR.name,syncfile)

                # There is a problem here. Google sheets add ^M to the end as
                # newlines. 
                with open(candidate, 'wb') as f:
                    f.write(r.content)
                    f.close()

                origfile=os.path.join(
                  config['gitdir'],
                  config['targetdir'],
                  sources[syncfile]['folder'],
                  "{}.csv".format(syncfile),
                  )

                if not filecmp.cmp(candidate, origfile):
                    debug("Found different files: "
                          "{}. Overwriting.".format(syncfile),
                         2)
                    changed_files.append(origfile)

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
        return commit_files(changed_files)
    else:
        debug("All files are the same. Not committing.", 2)
        return False


# ------------------------------------
def commit_files(changed_files):
    """ Commit set of changed_files to Git. Return True iff 
        files are committed.
    """
    committed_changes = False

    if config['no_commit']:
        debug("--no-commit specified, so not committing.", 2)
    else:
        try: 
            ssh_cmd = "ssh -i {}".format(config['github_ssh_key'])
            repo = Repo(config['gitdir'])
            with repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):

                origin = repo.remote('origin')
                origin.pull()

                changed_filenames = map(
                  lambda x: os.path.basename(x),
                  changed_files
                  )

                commit_msg = "Auto-commit: updated "
                commit_msg += "{} from Google Docs".format( 
                                 ", ".join(changed_filenames))

                debug(commit_msg, 1)

                repo.index.add(changed_files)
                repo.index.commit(commit_msg)
                origin.push()
                committed_changes = True
        except Exception as e: 
                    debug("Git exception:\n{}".format(e), 0)
                    raise
    return committed_changes



# ------------------------------------
def cleanup():
    """ Clean up file handles. """
    if DEBUG_FILEHANDLE:
        DEBUG_FILEHANDLE.close()

# --- END FUNCTIONS ---

args = parse_args()
global config
config = load_config(args)
setup_debug_log()

try: 
    debug("---- Beginning run ----",1)

    did_push = False
    did_sync = False

    if not config['no_download']:
        did_push = download_csvs()

        did_sync = sync_folders()
        

    # Check only on changed files, so that we do not get super-spammed with errors
    if did_push and not config['no_lint']:
        csv_lint.run_linter(config, DEBUG_FILEHANDLE)

    debug("---- Completed run ----",1)

except Exception as e: 
    debug("Got exception:\n{}".format(e), 0)
    raise

cleanup()

