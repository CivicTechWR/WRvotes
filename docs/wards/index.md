# Municipal Ward Listings

Each of the seven municipalities in Waterloo Region
are divided into wards. Clicking a ward will show all
the regional, municipal, and school board elections taking place in
that ward. 

If you would prefer a more graphical approach, use the [Ward
Map]({{site.url}}).

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


