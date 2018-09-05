CSV File Notes
--------------

- Commas are used to separate fields
- Double quotes are used to enclose fields that contain commas
- The encoding is UTF-8


Position IDs
------------

Position IDs (called "PositionUniqueName" in `nominees.csv` and
`position-tags.csv`) are the key to correlating information on the
site. They have the following properties: 

- Each position up for election ("race") gets a tag, and I guess the
  Cambridge Referendum does as well.
- Tags for ward councils are of the form `(Municipality)-Ward-XY`
  where `(Municipality)` is the municipality name and `XY` is a two
  digit identifier for the ward, with a possible leading zero. The two
  digits are important!
- No tag should be a substring of another tag, because sometimes we
  detect tag membership via searching in strings.
- Tags should be unique across the site. Each tag should refer to one
  race uniquely.

Positions for ward councils in each municipality are special. They are
associated with a municipality (a township or one of the three
cities). In Waterloo Region a ward is sufficient to identify all the
races in that region. 

Aliases
-------

Each position has a list of aliases. To sync with the Google calendar,
these aliases need to contain a substring that is in all aliases and
in no position tags. For us, that substring is "Alias-". 


Time and Date formats
---------------------

When specifying a date (for example, in `media-stories.csv`) then the
date should be in ISO date format. For example, to specify September 8
2018, write "2018-09-08". 

When specifying a date and a time, specify the time in 24-hour clock,
and divide the date and time with a capital T. Real ISO notation
prefers a timezone, but we will leave this off and assume local time.
For example, to specify 5:32pm on September 8, 2018, write
"2018-09-08T17:32"


Structure of _data Folder
-------------------------

There are two subfolders in the `_data` folder:

- `internal` contains data sources where the master copy is in this
  git repository. 
- `sync` contains data sources which must be synchronized from
  someplace else when there are changes (maybe an API, maybe a Google
  doc, maybe something else). Changes made within the repo might be
  blown away, so be careful!


Updating Candidate Info
-----------------------

As of this point, the `_data/sync/nominees.csv` must be
synchronized manually. It does not pull from a Google doc directly. It
also does not pull from the Region of Waterloo open data (sigh). 

Each candidate must be annotated with a position tag. There is not
currently a mechanism for linting this list to ensure that only valid
tags are entered (but there ought to be). 

When a candidate has been added correctly to this file, the candidate
lists on the website should be auto-updated. 


Adding Media Entries
--------------------

There are three kinds of media. One is news items, which are of interest
to people exploring deep into the election. One is opinion pieces. 

One is called "Questionnaires and Recorded Meetings" which is intended
to serve as side-by-side comparisons of candidates. These are the
resources that people hoping to make up their minds in a hurry should
use.

In `media.csv` these two types are distinguished by the
`ComparisonOrOpinion`
field. If this field is set to 'Comparison' then the entry will be included in
"Questionnaires and Recorded Meetings". If it is 'Opinion' it will be
marked as an opinion piece. Otherwise it is a regular news item. 

Note that capitals count!

Adding Event Entries
--------------------

Each event has a RowID. This must be distinct from all other rows.
They do not need to be in increasing order, but it does not hurt. 

Removing Event Entries
----------------------

You probably do not want to delete an event from events.csv, or the
Google Calendar will not reflect the change. Instead, marked the
"CancelledOrRescheduled" field to "Cancelled". 

Adding Menu Entries
-------------------

There are two steps. First, create your new page file in the `ocs`
directory. Then update `_data/internal/menu-layout.yml` . Spacing
is important, so follow the examples.


Changing the Map
----------------

The map is in GeoJSON format. Github pages has the ability to display
the map directly (but I think it lacks other features, such as street
address lookup). 

The original source comes from the Open Data portal. It is then
modified in a GeoJSON editor -- Todd suggests geojson.io, but Google
"My Maps" can also work.

Collapsing Sections with Buttons
--------------------------------

If you add a class `togglable` to a `div` or `ul` or any other
element, and you include the `hide-listings.js` in your page, then
buttons will show up to hide and unhide that element. 

- You may need additional `div` elements to prevent the page from
  looking gross when elements get hidden.
- Your element should contain a unique ID on the page.
- Your element may include other classes. All classes except
  `togglable` will be added to the button, for easy styling. 
- There is code in the javascript which changes the labels of the
  button, depending on which classes are included for the button. If
  no classes match the word "Results" is used.
- All togglable entries are set to collapsed by default
- Many lists will show some entries when collapsed. There is special
  code to sneakily generate multiple `ul` tags for this: see
  `_includes/list-event-block.html` for an example.


Adapting This Code for Your Municipality/Election
-------------------------------------------------

The code is fairly abstract. Most of the site-specific customization
is in the CSV files and in `_config.yml` . Here are exceptions where
things that are local to Waterloo Region are hardcoded: 

- The sharing links in the footer have hashtags specific to Waterloo
  Region
- The map embedding uses lat and long values specific to Waterloo
  Region
- The exceptions in `scripts/travis_build` have exceptions specific to
  the Waterloo Region dataset.

Javascript Libraries
--------------------

https://github.com/stefanocudini/leaflet-search

https://unpkg.com/leaflet@1.3.0/dist/leaflet.js

Travis CI
---------

Travis-CI is a continuous integration service that is free for open source 
projects like ours. It will run a series of basic tests on the CivicTechWR
website after building it with Jekyll. They will run on every build for 
any repository that is connected to their service and configured approprately.
Currently, travis will only run tests on branches named "master" and "dev".

To get started:
- Go to travis-ci.com and click "Sign up with GitHub"
- Accept the authorization from the Travis CI service. You will be redirected 
to Github
- Click the green Activate button, and select your CivicTechWR repository.

Now you should be able to check in to your dev branch and watch the CI
pipeline do it's thing. We suggest always doing your work in a feature branch
and periodically integrating into your dev branch whenever you want to ensure
you haven't broken things.

Configuration for Travis is all in the .travis.yml file. It runs the bash
scripts "scripts/build_site" and "scripts/travis_test" to do the actual
work of building and testing.

Tests
-----

We currently are running html-proofer in the CI pipline. It will test for
- broken internal links
- broken external links
- images referenced exist
- css and js resources exist

If there are more tests that you would like to see (if you have a specific 
component, for example) talk to us on Slack.
