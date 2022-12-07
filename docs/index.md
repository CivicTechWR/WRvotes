---
title: Welcome!
layout: default
use-leaflet: true
---

<section class="flex justify-center">
  <article class="standout-box blue large">
    <div class="big-text header" id="map-box" data-aos="fade-left">
    Election Day <strong>was</strong> October 24, 2022.
    </div>
    <div data-aos="fade-left">
    {% comment %}
    Use this site for information about the election, and the
    candidates asking for your vote!
    {% endcomment %}
    <p>
    <strong>Update, Dec 7:</strong> Added results of Cambridge/North
    Dumfries WCDSB election, and tallies for the French school boards
    as certified by the City of Kitchener (Catholic Board) and City of
    London (Public Board).
    </p><p>
    <strong>Update, Nov 5:</strong> Added voting period for WCDSB
    election.
    </p><p>
    <strong>Update, Oct 25:</strong> We have updated the site with
    unofficial vote counts and winners for many races, excluding the
    French language school boards, and the suspended race.
    </p>
    </div>
    <div class="countdown-container" style="font-size: 1.5rem; margin-bottom: 48px;" data-aos="fade-left">
      <div class="countdown-days">
      </div>
    <!--Today is Election Day-->
    </div>
    <div class="content" data-aos="fade-up">
     <p>Type your address to identify your ward, or click your
     location on the map. (Note that although the address lookup is
     pretty good, it is not 100% accurate, especially near ward
     boundaries. If in doubt consult your <a
     href="https://wrvotes.com" target="_blank">municipality</a>.)</p>
     <div id="map-searchbar"></div>
     <div id="map"></div>
     <p><strong>Note:</strong> The map loads more slowly than the rest
     of the page, so be patient, or use the <a href="/wards/">ward listing</a>.</p>
    </div>
  </article>
</section>

<script src="{{ site.baseurl }}/assets/js/leaflet.js"></script>
<script src="{{ site.baseurl }}/assets/js/leaflet-search.min.js"></script>
<!-- This has too many dependencies to load locally. -->
<script src="https://unpkg.com/leaflet-pip@1.1.0/leaflet-pip.js"></script>
<script src="{{ site.baseurl }}/assets/js/jquery-3.6.0.min.js"></script>
<script src="{{ site.baseurl }}/assets/js/show-map.js"></script>
