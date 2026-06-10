#!/bin/bash 

# $1 is the virtualenv path
# $2 is the path to the script
# $3 is the config file for get-csv
# $4 is the config file for update-google-calendars
# https://stackoverflow.com/questions/4150671

source $1/bin/activate
# Yikes.
cd $2
python3 gdocs-get-csv.py --configfile $3
#python3 update-google-calendar.py --configfile $4


# Sample crontab entry
# Update WRV information 
#1,16,31,46 * * * * /home/pnijjar/WRVotesPlaceholder/scripts/run_update_scripts.sh /home/pnijjar/WRVotesPlaceholder/scripts/venv/ /home/pnijjar/WRVotesPlaceholder/scripts/ /home/pnijjar/WRVotesPlaceholder/scripts/gdocs-get-csv.config.yml /home/pnijjar/WRVotesPlaceholder/scripts/update-google-calendar.config.py | /home/pnijjar/WRVotesPlaceholder/scripts/maybe-send-mail.sh civictechwr.wrvotes@gmail.com "Google Sheets validation problem" 

