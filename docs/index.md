---
title: Home
layout: default
use-leaflet: true
---

<section class="flex">
  <article class="standout-box pink medium">
    <div class="big-text pink-text header" data-aos="fade-left">
      On October 22, 2018 there will be a municipal election in Waterloo Region.
    </div>
    <div class="content" data-aos="fade-right">
      <p>Municipal elections can be confusing.</p>
      <p>There are a lot of positions to vote for! There are no political parties! How do you start educating yourself so you can cast an informed vote?</p>
    </div>
  </article>
</section>

<section class="flex justify-right">
  <article class="standout-box blue medium">
    <div class="big-text blue-text header" data-aos="fade-left">Don't panic. We've got you covered.</div>
    <div class="content" data-aos="fade-right">
      <p>Start by looking up the candidates who are running in your area.
        Use the map below to <strong>locate your <a href="/wards/">municipal ward</a></strong>, and click the
      information link. From here you will find a list of the candidates for every position you can
        vote for.</p>
      <p>If you are unsure of <strong>what is going on</strong>, or wonder<strong> why you should care</strong>, check out our <a href="/resources">resource pages</a> for useful background information about the election.</p>
    </div>
  </article>
</section>

<section class="flex justify-center">
  <article class="standout-box green large" id="map-box">
    <div class="big-text green-text header" data-aos="fade-left">Start by finding your ward.</div>
    <div class="content" data-aos="fade-right">
      <p>The map loads more slowly than the rest of the page, so be
      patient, or use the <a href="/wards/">ward listing</a>.</p>
      <p><strong>Important</strong>: The ward boundaries on this map are close but not exact. If you live close to a boundary you need to double-check which ward you are in.</p>
      <div id="map-searchbar"></div>
      <div id="map"></div>
    </div>
  </article>
</section>



<script src="{{ site.baseurl }}/assets/js/leaflet.js"></script>
<script src="{{ site.baseurl }}/assets/js/leaflet-search.min.js"></script>
<!-- This has too many dependencies to load locally. -->
<script src="https://unpkg.com/leaflet-pip@1.1.0/leaflet-pip.js"></script>
<script src="{{ site.baseurl }}/assets/js/jquery-3.3.1.min.js"></script>
<script src="{{ site.baseurl }}/assets/js/show-map.js"></script>
