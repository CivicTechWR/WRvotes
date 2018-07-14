---
---

Attempt: 18

{% comment %}
Try to eat up all leading slashes and the trailing .html . 
This is gross but it works.
{% endcomment %}
{% assign ward-id = page.url | replace: '.html', '' | split: '/' | last -%}
{% assign ward-info = site.data.site-data.position-tags |
where:"PositionUniqueName",ward-id | first -%}

Title: {{ page.title }} 

URL: {{ page.url }}

Ward ID: {{ ward-id }}

Ward Info: {{ ward-info }}

## Running in this Ward

{% for nominee in site.data.site-data.nominees 
where:"PositionUniqueName",ward-id | sort: 'Last_Name','Given_Names'
%}
- {% if nominee.Website -%}
  [{{ nominee.Given_Names }} 
    {{ nominee.Last_Name }}]({{ nominee.Website }})
  {%- else -%}
    {{ nominee.Given_Names}} {{ nominee.Last_Name }}
  {%- endif -%}
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
