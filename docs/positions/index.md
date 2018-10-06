---
layout: default
title: Elected Position Listing
---

# Elected Position Listing 

This list links to pages for each available elected position
in the election, and a few information pages. Each page includes
nominee listings, news articles, questionnaires, and meeting
informations relevant to that position. 

<ul>
  {% for position in site.data.internal.position-tags %}
      <li><a href="./{{ position.PositionUniqueName }}">{{ position.PositionDesc }}</a></li>
  {% endfor %}
</ul>



