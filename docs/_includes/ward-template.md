---
title: Some Title
---
Title: {{ page.title }} 

URL: {{ page.url }}

{% assign ward-name = page.url | match_regex: '(.)"\.html' %}

Ward Name: {{ ward-name }}

Path: {{ page.path }} 

ID: {{ page.id }}

Categories: {{ page.categories }}

All posts in Wards: {{ site.categories.ward }}

## All positions: 

{% for position in site.data.site-data.position-tags %}
- {{ position.PositionUniqueName }} : {{ position.PositionDesc }}
{% endfor %}

## All nominees: 

{% for nominee in site.data.site-data.nominees %}
- {{ nominee.Given_Names }} {{ nominee.Last_Name }} : 
  {{- nominee.PositionUniqueName }}
{% endfor %}
