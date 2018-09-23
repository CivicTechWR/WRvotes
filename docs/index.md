---
title: Welcome!
layout: default
use-leaflet: true
---

<section class="flex justify-center">
  <article class="standout-box pink medium">
    <div class="big-text pink-text header" id="map-box" data-aos="fade-left">
      On October 22, 2018 there will be a municipal election in Waterloo Region.
    </div>
    <div class="content" data-aos="fade-up">
     <p>Get informed, then vote! Type your address to find your ward, and click the information link in the pop up to learn about your local candidates. More information about <strong>why</strong>, <strong>how</strong>, &amp; <strong>where</strong> to vote can be found in the <a href="/resources">resources section</a> of the site. The <a href="/events">events</a> page has a calendar showing times and places where you can meet candidates and ask them questions in person.</p>
     <p><strong>Note:</strong> The ward boundaries on this map are more visually accurate the closer you zoom in. If you live close to a boundary, double check which ward you are in. The map loads more slowly than the rest of the page, so be patient, or use the <a href="/wards/">ward listing</a>.</p>
    </div>
  </article>
</section>

<script src="{{ site.baseurl }}/assets/js/leaflet.js"></script>
<script src="{{ site.baseurl }}/assets/js/leaflet-search.min.js"></script>
<!-- This has too many dependencies to load locally. -->
<script src="https://unpkg.com/leaflet-pip@1.1.0/leaflet-pip.js"></script>
<script src="{{ site.baseurl }}/assets/js/jquery-3.3.1.min.js"></script>
<script src="{{ site.baseurl }}/assets/js/show-map.js"></script>
