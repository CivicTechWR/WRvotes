#!/bin/bash 

# $1 is the virtualenv path
# $2 is the path to the script
# $3 is the config file for get-csv
# $4 is the config file for update-google-calendars
# https://stackoverflow.com/questions/4150671

source $1/bin/activate
# Yikes.
cd $2
python3 get-csv.py --configfile $3
python3 update-google-calendar.py --configfile $4


# Sample crontab entry
# Update WRV information 
#1,16,31,46 * * * * /home/pnijjar/WRVotesMunicipal2022/scripts/run_update_scripts.sh /home/pnijjar/WRVotesMunicipal2022/scripts/venv/ /home/pnijjar/WRVotesMunicipal2022/scripts/ /home/pnijjar/WRVotesMunicipal2022/scripts/get-csv-config.yml /home/pnijjar/WRVotesMunicipal2022/scripts/update-google-calendar.config.py >> /home/pnijjar/logs/cronjob.log
