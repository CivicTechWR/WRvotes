
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

TODO: Include email addresses and phone numbers for the candidates. 


Position Tags
-------------

Every candidate running for office has a position. Every position has
an associated tag, which must be one of the tags in
`_data/internal/position-tags.csv` . If you want to add a new
position, you must update this CSV file. 

Positions for ward councils in each municipality are special. They are
associated with a municipality (a township or one of the three
cities). In Waterloo Region a ward is sufficient to identify all the
races in that region. 


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
