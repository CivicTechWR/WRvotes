---
layout: default
title: 2018 Results
---

# Election Results


<div class="wrv-accordion" data-aos="fade-up">
    {% for municipality in site.data.internal.municipality-map %}
        <div class="accordion-ward">
            <a>{{municipality.MunicipalityType}} of {{municipality.Name}}</a>
            <div class="content">
                /** cards go here **/
                <p>Lorem Ipsum </p>
            </div>
        </div>
    {% endfor %}
</div>



<script src="{{ site.baseurl }}/assets/js/accordion.js"></script>