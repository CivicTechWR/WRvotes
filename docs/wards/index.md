---
layout: default
title: Ward List
---

# Ward List

Click a ward to show the
candidates running there. For a more graphical approach, use the 
[Interactive Map]({{site.url}}).

{% assign ridings-sorted = site.data.internal.position-tags | 
sort: "PositionUniqueName" | 
where_exp: "item", "item.PositionUniqueName contains '-Ward-'" %}
<div class="content-box" data-aos="fade-up">
  <ul>
    {% for riding in ridings-sorted %}
      <li><a href="./{{ riding.PositionUniqueName }}">{{ riding.PositionDesc }}</a></li>
    {% endfor %}
  </ul>
</div>
