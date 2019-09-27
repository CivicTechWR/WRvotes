Deployment
----------

- Generate a Google service account. It needs access to the Calendar API, but does not need roles. 
  + <https://console.developers.google.com>
  + Make a project
  + Make a service account
  + Give the service account access to the Calendar API
  + In the Google Calendar, give the email address of the service
  account "Make Changes to Events" permissions
- Use `virtualenv` to set up a Python 3 environment: `virtualenv -p
  /usr/bin/python3 venv`
- Activate the environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Copy `update-google-calendar.config.py.example` to `update-google-calendar.config.py` and customize it to your
  needs.

- Run `update-google-calendar.py`


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
  `git clone git@github.com:CivicTechWR/WRVotesFed wrvotesfed`
- `cd wrvotesfed`
- Add cronjob to force a rebuild every N minutes
