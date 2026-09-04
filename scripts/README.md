Google Account Setup
--------------------

You can use the same credentials for downloading CSVs, updating the
calendar, and syncing from Drive. 


- Generate a Google service account. It needs access to the Calendar API, but does not need roles. 
  + <https://console.developers.google.com>
  + Make a project
  + Make a service account
  + Visit <https://console.cloud.google.com/apis/dashboard>
  + Give the service account access to:
    + the Calendar API
    + the Drive API
  + Create JSON credentials for the account
    * Set API restrictions to Calendar API
    * Also to Drive API

  + In the Google Calendar, give the email address of the service
  account "Make Changes to Events" permissions

  + In the Google Drive, give the email address of the service viewer
  permissions to the folders that are to be synced.


Deployment (update-google-calendar)
-----------------------------------

- Use `virtualenv` to set up a Python 3 environment: `virtualenv -p
  /usr/bin/python3 venv`
- Activate the environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Copy `update-google-calendar.config.yml.example` to
  `update-google-calendar.config.yml` and customize it to your
  needs.

- Run `update-google-calendar.py --configfile
  update-google-calendar.config.yml`



Deployment With Cron onto Github
--------------------------------

- Make a virtualenv and install the necessary Python packages:
  ```
  virtualenv -p python3 venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- Make sure there is an appropriate SSH key in the VPS
- Add SSH Deploy key to the project.
- On the VPS, check out the code:
  `git clone git@github.com:CivicTechWR/WRVotesMunicipal2022 wrvotes`
- `cd wrvotes`
- Add cronjob to force a rebuild every N minutes

[ADD CRONJOB LINE]
