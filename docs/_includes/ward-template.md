---
title: Some Title
---
Title: {{ page.title }} 

URL: {{ page.url }}

Path: {{ page.path }} 

ID: {{ page.id }}

Categories: {{ page.categories }}

All posts in Wards: {{ site.categories.ward }}

All positions: 

{% for position in site.data.site-data.position-tags %}
- {{ position.PositionUniqueName }} : {{ position.PositionDesc }}
{% endfor %}
