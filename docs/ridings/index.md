---
layout: default
title: Riding List
---

# Riding List

There are five ridings in Waterloo Region. Click a riding to show the
candidates running there. For a more graphical approach, use the 
[Riding Map]({{site.url}}).

{% assign ridings-sorted = site.data.internal.position-tags | sort: "PositionUniqueName" %}
<div class="content-box" data-aos="fade-up">
  <ul>
    {% for riding in ridings-sorted %}
      <li><a href="./{{ riding.PositionUniqueName }}">{{ riding.PositionDesc }}</a></li>
    {% endfor %}
  </ul>
</div>
