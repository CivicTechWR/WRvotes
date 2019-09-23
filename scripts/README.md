Deployment
----------

- Generate a Google service account. It needs access to the Calendar API, but does not need roles. 
- Use `virtualenv` to set up a Python 3 environment: `virtualenv -p
  /usr/bin/python3 venv`
- Activate the environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Copy `update-google-calendar.config.py.example` to `update-google-calendar.config.py` and customize it to your
  needs.

- Run `update-google-calendar.py`


Deployment With Cron onto Github
--------------------------------

- Make sure there is an appropriate SSH key in the VPS
- Add SSH Deploy key to the project.
- On the VPS, check out the code:
  `git clone git@github.com:CivicTechWR/WRVotesFed wrvotesfed`
- `cd wrvotesfed`
- Add cronjob to force a rebuild every N minutes
