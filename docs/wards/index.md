---
layout: default
title: Find Your Candidates
---

# Find Your Candidates 

Your city or township is divided into **wards**. If you know your ward
we can show you all the candidates running for **regional**, **school
board** and **local municipality** positions where you live. 

If you would prefer a more graphical approach, use the [Ward
Map]({{site.url}}).

{% for municipality in site.data.internal.municipality-map %}
  <div class="content-box" data-aos="fade-up">
    <h2 class="toggleable" >{{municipality.MunicipalityType}} of {{municipality.Name}}</h2>

    {% assign wards-unsorted = site.data.internal.position-tags
      | where: "WardMunicipality",municipality.Name %}
    {% assign wards-sorted = wards-unsorted | sort: "PositionUniqueName" %}

    <ul class="toggle-content" >
    {% for ward in wards-sorted %}
      <li><a href="./{{ ward.PositionUniqueName }}">{{ ward.ShortLocalDesc }}</a></li>
    {% endfor %}
    </ul>
  </div>

{% endfor %}


