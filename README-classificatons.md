What is fair game for the site? What goes where?
================================================

Reducing Duplicates
-------------------

There are two options to deal with events, questionnaires, articles,
etc that apply to many positions.

If it is not important that this event be listed for every single race
(eg mayor and ward councillors) then list the position that is the
most general position. 

For example, articles about all of Cambridge can be tagged 
"Cambridge-Mayor" and articles about all of Waterloo Region can be
tagged "Regional-Chair"

If it is important that this event be listed in all races (most
all-candidates meetings, probably most questionnaires) then you can
use an alias. Each position has a list of applicable aliases in
`position-tags.csv` , and you can use one of them. 


Note that the Election-Info tag is strictly for information about the
election.


Events
------

- Events should be related to candidate campaigning in some way
- Events from individual candidates may be posted, but must not have
  anything in ForMultipleCandidates
- Rule of thumb: if the event is for a candidate's supporters only, it
  is not eligible for the calendar. If the event is for all people
  (including people opposed to the candidate) then it is okay.

Media
-----

The field `ComparisonOrOpinion` has been renamed to `Category`. 

We are now public with how we classify media items. See
`docs/philosophies/media-inclusion.md` for these criteria. 

All media pieces should have one of the following classifications:

- `AllCandidates` for debate and all-candidate meeting recordings

- `Questionnaires` for questionnaires. We no longer include
  endorsement lists in this category. 

- `CandidateProfiles` for publications that include one or more
  candidates for a race. 

- `Opinion` for opinion pieces, which can include group discussions
  like Reddit threads, newspaper articles by opinion columnists, and
  endorsement lists. 

- `Article` for everything else, which includes news items produced by
  established news media. These are usually about election-related
  news (eg Jan Liggett broke her leg). 

- `ElectionResults` for the flood of articles telling us how the
  election turned out. 

- News items that are about election issues (safe injection sites,
  intensification) but not about the election directly usually do not
  belong here. 
  There is a page `issues-overview.md` which publishes A FEW
  (2-4) links per issue. Tag these articles with `Issue` as the
  PositionIDList and one of the tags in `issues-categories.csv` as the
  Category.

### Fuzzy lines

- Letters to the editor? Probably not.
- News articles outside the mainstream? Maybe. The standard for
  marking as news and not opinion should be relatively high (ie the
  article should be fair to all sides)
