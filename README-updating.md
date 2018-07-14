Updating Candidate Info
-----------------------

As of this point, the `_data/site-data/nominees.csv` must be
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
`_data/site-data/position-tags.csv` . If you want to add a new
position, you must update this CSV file. 

Positions for ward councils in each municipality are special. They are
associated with a municipality (a township or one of the three
cities). In Waterloo Region a ward is sufficient to identify all the
races in that region. 



Adding Menu Entries
-------------------

There are two steps. First, create your new page file in the `ocs`
directory. Then update `_data/site-config/menu-layout.yml` . Spacing
is important, so follow the examples.
