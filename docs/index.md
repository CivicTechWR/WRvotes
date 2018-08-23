---
title: Home
use-leaflet: true
---

<section class="flex">
  <article class="standout-box pink medium" data-aos="fade-up">
    <div class="big-text pink-text">
      On October 22, 2018 there will be a municipal election in Waterloo Region.
    </div>

    <p>Municipal elections can be confusing.</p>
    <p>There are a lot of positions to vote for! There are no political parties! How do you start educating yourself so you can cast an informed vote?</p>
  </article>
</section>

<section class="flex justify-right">
  <article class="standout-box yellow medium" data-aos="fade-up">
    <div class="big-text yellow-text">Don't panic. We've got you covered.</div>

    <p>Start by looking up the candidates that are running in your area.
    Use the map below to <strong>locate your municipal ward</strong>, and click the
    information link. This will pop up a list of every position you can
    vote for (including regional candidates, your mayor, and school board
    trustees).</p>

    <p>If you don't like maps (or don't have Javascript enabled on your
    browser), you can find a page for your ward in our <a href="/wards/">ward
    listing</a>.</p>


    <p>Along with candidate listings you will find links to upcoming events,
    news articles, and other information that can help you get up to speed
    quickly.</p>

    <p>Also, check out our <a href="/resources">resource pages</a>. They contain lots of good
    background information about the election. If you don't know <strong>what is
    going on</strong>, or <strong>why you should care</strong>, you will find answers here.</p>
  </article>
</section>

<section class="flex justify-center">
  <article class="standout-box blue large" data-aos="fade-up" id="map-box">
    <div class="big-text blue-text">Start by finding your ward.</div>
    <p>The map loads more slowly than the rest of the page, so be
    patient, or use the <a href="/wards/">ward listing</a>.</p>
    <p><strong>Important</strong>: The ward boundaries on this map are close but not exact. If you live close to a boundary you need to double-check which ward you are in.</p>
    <script src="https://embed.github.com/view/geojson/CivicTechWR/WRvotes/master/docs/_data/sync/WardBoundaries.geojson?height=500&width=640"></script>
  </article>
</section>


<div id="map-searchbar"></div>
<div id="map">
</div>


<script src="{{ site.baseurl }}/assets/js/leaflet.js"></script>
<script src="{{ site.baseurl }}/assets/js/leaflet-search.min.js"></script>
<!-- This has too many dependencies to load locally. -->
<script src="https://unpkg.com/leaflet-pip@1.1.0/leaflet-pip.js"></script>
<script src="{{ site.baseurl }}/assets/js/jquery-3.3.1.min.js"></script>
<script src="{{ site.baseurl }}/assets/js/show-map.js"></script>
