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

The field `ComparisonOrOpinion` has been renamed to `Category`. All
media pieces should have one of the following classifications:

- `AllCandidates` for debate and all-candidate meeting recordings
- `Questionnaire` for questionnaires. Questionnaires are standard
  questions for all candidates, answered by the candidates in their
  own words.
- `EndorsementList` for endorsements by advocacy groups. (There is
  some fuzziness here between endorsements and opinions.)
- `ProfileList` for single publications that list several or all
  candidates for a race. The distinction between these and
  `Questionnaires` is that the reporters paraphrase reponses from the
  candidates, or the pieces do not consist of structured questions.
- `SingleProfile` for articles profiling individual candidates. There
  can be fuzziness here with `Questionnaires` -- some publications ask
  standard questions of candidates, but devote one URL per candidate.
  We classify each response as a `SingleProfile`
- `Opinion` for opinion pieces, which can include group discussions
  like Reddit threads, or newspaper articles by opinion columnists.
  (Some opinion columnists also write `SingleProfile` pieces on
  individual candidates.)
- `Article` for everything else, which includes news items produced by
  (formal or informal) news media. There is some fuzziness between
  `Article` and `Opinion`. Articles should strive to be fair to all
  sides. 
- News items that are about election issues (safe injection sites,
  intensification) but not about the election directly are probably
  not fair game. 

### Fuzzy lines

- Letters to the editor? Probably not.
- News articles outside the mainstream? Maybe. The standard for
  marking as news and not opinion should be relatively high (ie the
  article should be fair to all sides)
