---
title: Welcome!
layout: default
use-leaflet: true
---

<section class="flex justify-center">
  <article class="standout-box blue large">
    <div class="big-text blue-text header" id="map-box" data-aos="fade-left">
    October 22, 2018 <strong>was</strong> municipal election day in Waterloo Region.
    </div>
    <div class="content">
    <p>Because internet voting is amazing, the townships of Woolwich
    and Wellesley have extended their voting period to <strong>8pm on
    Tuesday, October 23</strong>. For this reason, results for
    Regional Chair and some school trustee positions 
    will not be available until Wednesday morning.
    </p><p>
    Here are unofficial results for the other municipalities. 
    <ul>
      <li><a
      href="https://www.cambridge.ca/Modules/News/index.aspx?newsId=3ff966f5-bf66-4ed4-abff-3b0b7f2ca521">City of Cambridge</a></li>
      <li><a
      href="https://www.kitchener.ca/Modules/News/index.aspx?newsId=b2f62478-c62c-4d9e-8655-643c32c2c1ea">City of Kitchener</a></li>
      <li><a
      href="https://www.northdumfries.ca/en/township-services/2018-election-results.aspx">Township of North Dumfries</a></li>
      <li><a
      href="https://www.wilmot.ca/en/township-office/election-day-results.aspx">Township of Wilmot</a></li>
      <li><a
      href="https://www.waterloo.ca/en/contentresources/resources/government/Elections/2018-Elections/unofficial-election-results-2018.pdf">City
      of Waterloo</a> (PDF)</li>
    </ul>
    </p>
    </div>
    <div class="content" data-aos="fade-up">
     <p>Type your address to find information about candidates & events relevant to your ward. Get informed, then vote!</p>
     <div id="map-searchbar"></div>
     <div id="map"></div>
     <p><strong>Note:</strong> The map loads more slowly than the rest of the page, so be patient, or use the <a href="/wards/">ward listing</a>.</p>
    </div>
  </article>
</section>

<script src="{{ site.baseurl }}/assets/js/leaflet.js"></script>
<script src="{{ site.baseurl }}/assets/js/leaflet-search.min.js"></script>
<!-- This has too many dependencies to load locally. -->
<script src="https://unpkg.com/leaflet-pip@1.1.0/leaflet-pip.js"></script>
<script src="{{ site.baseurl }}/assets/js/jquery-3.3.1.min.js"></script>
<script src="{{ site.baseurl }}/assets/js/show-map.js"></script>
