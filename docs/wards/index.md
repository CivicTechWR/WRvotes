# Municipal Ward Listings

Attempt: 02

Each of the seven municipalities in Waterloo Region (Cambridge,
Kitchener, North Dumfries, Waterloo, Wellesley, Wilmot, and Woolwich)
are divided into wards, listed below. Clicking a ward will show all
the regional, municipal, and school board elections taking place in
that ward. 

If you would prefer a more graphical approach, use the [Ward Map](/).

{% for municipality in site.data.internal.municipality-map %}
  <h2>{{municipality.MunicipalityType}} of {{municipality.Name}}</h2>

  {% assign wards-unsorted = site.data.internal.position-tags 
    | where: "WardMunicipality",municipality.Name %}
  {% assign wards-sorted = wards-unsorted | sort: "PositionUniqueName" %}

  <ul>
  {% for ward in wards-sorted %}
    <li><a href="./{{ ward.PositionUniqueName }}">{{ ward.PositionDesc }}</a></li>
  {% endfor %}
  </ul>

{% endfor %}


