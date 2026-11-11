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


Deployment (Google sync scrupts)
-----------------------------------

To deploy this we have been using a cronjob on a separate VPS, with
the Github code checked out locally. There are other ways. You could
probably sync with Github Actions but we did not do this. 

- Make sure there is an appropriate SSH key in the VPS
- Add SSH Deploy key to the project.
- On the VPS, check out the code:
  `git clone git@github.com:CivicTechWR/WRVotesMunicipal2022 wrvotes`
- `cd wrvotes`


- Use `virtualenv` to set up a Python 3 environment: `virtualenv -p
  /usr/bin/python3 venv`
- Activate the environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Copy `update-google-calendar.config.yml.example` to
  `update-google-calendar.config.yml` and customize it to your
  needs.
- Do the same with `gdocs-get-csv.config.yml`

- Set up a cronjob to run the scripts. See the source of
  `run-update-scripts.sh` for an example. 



