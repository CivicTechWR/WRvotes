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

- News articles from mainstream (lamestream?) media sources count as
  news.
- All candidate surveys count and should be tagged with IsComparison
- Meeting recordings of all-candidates meeting should be tagged with
  IsComparison
- News opinion pieces by columnists are fair game but must be marked
  "Opinion"
- News items that are about election issues (safe injection sites,
  intensification) but not about the election directly are probably
  not fair game. 

### Fuzzy lines

- Letters to the editor? Probably not.
- Arbitrary opinions on blogs? Dunno. Maybe they count as opinions.
- News articles outside the mainstream? Maybe. The standard for
  marking as news and not opinion should be relatively high (ie the
  article should be fair to all sides)
