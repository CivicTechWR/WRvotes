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
    <p>
    Here are unofficial results from the municipalities.
    <ul>
      <li><a
      href="https://www.regionofwaterloo.ca/en/regional-government/results.aspx">Region of Waterloo </a></li>
      <li><a
      href="https://www.cambridge.ca/Modules/News/index.aspx?newsId=3ff966f5-bf66-4ed4-abff-3b0b7f2ca521">City of Cambridge</a></li>
      <li><a
      href="https://www.kitchener.ca/Modules/News/index.aspx?newsId=b2f62478-c62c-4d9e-8655-643c32c2c1ea">City of Kitchener</a></li>
      <li><a
      href="https://www.northdumfries.ca/en/township-services/2018-election-results.aspx">Township of North Dumfries</a></li>
      <li><a
      href="https://www.wellesley.ca/en/elections/2018-election-results.aspx">Township of Wellesley</a></li>
      <li><a
      href="https://www.wilmot.ca/en/township-office/election-day-results.aspx">Township of Wilmot</a></li>
      <li><a
      href="https://www.woolwich.ca/en/elections/elections-2018.aspx">Township of Woolwich</a></li>
      <li><a
      href="https://www.waterloo.ca/en/government/election.asp">City of Waterloo</a></li>
    </ul>
    </p>
    </div>
    <div class="content" data-aos="fade-up">
     <p>In the meantime, we intend to keep waterlooregionvotes.org
     up and running as a reference for the future. 
     Type your address to find information about candidates & events relevant to your ward.</p>
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
