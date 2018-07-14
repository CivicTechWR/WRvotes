---
title: Some Title
---
Attempt: 04

Title: {{ page.title }} 

URL: {{ page.url }}

{% comment %} 
Try to eat up all leading slashes. Don't allow periods in 
ward names, and ignore everything after the period. 
{% endcomment %}
{% assign ward-name = page.url | match_regex: '^(?:.+)\/(.+)\.(?:.+)$' %}
{% assign ward-explore = page.url | match_regex: '.+(\d\d).+' %}

Ward Name: {{ ward-name }}

Ward Exploration: {{ ward-explore }}

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
