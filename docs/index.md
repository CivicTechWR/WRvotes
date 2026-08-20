---
title: Welcome!
layout: default
use-leaflet: true
---

<section class="flex justify-center">
  <article class="standout-box blue large">
    <div class="big-text header" id="map-box" >
    The Municipal Election is October 26, 2026
    </div>

    <p>Use this website to learn about the municipal election, and the
    candidates asking for your vote.
    </p><p>
    If you are feeling overwhelmed or confused
    you can start by reading the <a href="./resources/voter-info">Information 
    for Voters</a> page. 
    </p>

    <div class="content" data-aos="fade-up">
     <p>
     <strong>Type your address to find your candidates, or click your
     location on the map.</strong>
     </p>

     <div class="map-loader" aria-live="polite" data-baseurl="{{ site.baseurl }}">
       <p id="map-loader-status" class="map-loader-status">
         Loading the interactive ward map.
       </p>
     </div>
     {% if site.enable-map-search-nominatim %}
       <div id="map-searchbar"></div>
     {% endif %}

     <div id="map"></div>


     <p>If the map is loading slowly or does
     not load, please use the <a href="/by-ward/">text ward listings</a>.
     </p>
     <p>
     (Note that although the address lookup is
     pretty good, it is not 100% accurate, especially near ward
     boundaries. If in doubt consult your <a href="https://wrvotes.com" 
     target="_blank">municipality</a>.)
     </p>

    </div> <!-- Data AOS -->

  </article>
</section>

<script defer src="{{ site.baseurl }}/assets/js/home-map-loader.js"></script>
