
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
