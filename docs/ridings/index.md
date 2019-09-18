---
layout: default
title: Riding List
---

# Riding List

Waterloo Region is divided into 5 ridings. Click a riding to show all of the nominees
running in that riding.


If you would prefer a more graphical approach, use the [Riding Map]({{site.url}}).

{% assign ridings-sorted = site.data.internal.position-tags | sort: "PositionUniqueName" %}
<div class="content-box" data-aos="fade-up">
  <ul>
    {% for riding in ridings-sorted %}
      <li><a href="./{{ riding.PositionUniqueName }}">{{ riding.PositionDesc }}</a></li>
    {% endfor %}
  </ul>
</div>
