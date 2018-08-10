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
