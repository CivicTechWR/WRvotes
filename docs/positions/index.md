---
layout: default
title: Elected Position Listing
---

# Elected Position Listing 

This list links to pages for each available elected position
in the election, and a few information pages. Each page includes
nominee listings, news articles, questionnaires, and meeting
information relevant to that position. 

Note that these pages show information for only one position. If you
want to know who is running in the different races where you live, use
the [ward pages](/wards) instead.

<div class="content-box">
  <ul>
    {% for position in site.data.internal.position-tags %}
        <li><a href="./{{ position.PositionUniqueName }}">{{ position.PositionDesc }}</a></li>
    {% endfor %}
  </ul>
</div>


