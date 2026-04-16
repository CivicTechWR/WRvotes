---
title: Welcome!
layout: default
use-leaflet: true
---

<section class="flex justify-center">
  <article class="standout-box blue large">
    <div class="big-text header" id="map-box" data-aos="fade-left">
    The Municipal Election was October 22, 2022
    </div>
    <p>Use this website to learn about the municipal election, and the
    candidates asking for your vote. If you are feeling overwhelmed or
    confused you can start by reading the 
     <a href="./resources/getting-informed" target="_blank">getting
     informed</a> page for step-by-step guidance.
    </p>
    <div data-aos="fade-left">
     <p>Type your address to identify your ward, or click your
     location on the map. Once you have identified your ward you will
     be able to see the <strong>regional</strong>,
     <strong>municipality</strong> and <strong>school board</strong>
     candidates you can vote for.
     </p>
    </div>

    <div class="content" data-aos="fade-up">
     <p>
     (Note that although the address lookup is
     pretty good, it is not 100% accurate, especially near ward
     boundaries. If in doubt consult your <a
     href="https://wrvotes.com" target="_blank">municipality</a>.)</p>
     <div class="map-loader" aria-live="polite">
       <button id="load-map-button" class="load-map-button" type="button"
         data-baseurl="{{ site.baseurl }}">
         Load the interactive ward map
       </button>
       <p id="map-loader-status" class="map-loader-status">
         The map is loaded on demand to keep the homepage fast.
       </p>
     </div>
     <div id="map-searchbar" hidden></div>
     <div id="map" hidden></div>
     <p><strong>Note:</strong> The map loads more slowly than the rest
     of the page, so be patient, or use the <a href="/wards/">ward listing</a>.</p>
    </div>
  </article>
</section>

<script defer src="{{ site.baseurl }}/assets/js/home-map-loader.js"></script>
