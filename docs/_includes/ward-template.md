---
---

Attempt: 31

{% comment %}
Try to eat up all leading slashes and the trailing .html . 
This is gross but it works.
{% endcomment %}
{% assign ward-id = page.url | replace: '.html', '' | split: '/' | last -%}
{% assign ward-info = site.data.site-data.position-tags |
where:"PositionUniqueName",ward-id | first -%}

Ward Info: {{ ward-info }}

## Running in this Ward

{% assign municipal-info = site.data.site-data.municipality-map |
where:"Name",ward-info.WardMunicipality %}
{% assign races-unsplit = municipal-info.Races %}
{% assign races-split = races-unsplit | split: ',' %}

Municipal-info: {{ municipal-info }} 

Municipal-info.Races: {{ municipal-info.Races }}

Municipality Type: {{ municipal-info.MunicipalityType }}

Races.races: {{ races.Races }}

Races Unsplit: {{ races-unsplit }}

Race Array: {{ races-split }}

{% for race in races-split -%}
  {% if race == "_SELF" %}
    {% assign race = ward-id %}
  {% endif %}
  
  {% assign race-info = site.data.site-data.position-tags |
  where:"PositionUniqueName",race -%}

  ### {{ race-info.PositionDesc -}}
  
  {% assign these-nominees = site.data.site-data.nominees 
    | where:"PositionUniqueName",race %}
  {% assign sorted-nominees = these-nominees | sort: "Last_Name" %}

  {% for nominee in sorted-nominees %}
- {% if nominee.Website -%}
    [{{ nominee.Given_Names }} 
      {{ nominee.Last_Name }}]({{ nominee.Website }})
    {%- else -%}
      {{ nominee.Given_Names}} {{ nominee.Last_Name }}
    {%- endif -%}
  {% endfor %}

{% endfor %}


## All positions

{% for position in site.data.site-data.position-tags %}
- {{ position.PositionUniqueName }} : {{ position.PositionDesc }}
{% endfor %}

## All nominees 

{% for nominee in site.data.site-data.nominees %}
- {{ nominee.Given_Names }} {{ nominee.Last_Name }} : 
  {{- nominee.PositionUniqueName }}
{% endfor %}
