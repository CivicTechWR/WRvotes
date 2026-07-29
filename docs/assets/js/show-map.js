---
layout: none
---


window.WRVotesInitMap = async function(baseUrl) {
  var geojsonLayer = null;
  var mapRoot = document.getElementById("map");


  {% if site.enable-map-search-nominatim %}
      var searchRoot = document.getElementById("map-searchbar");
      searchRoot.hidden = false;
  {% endif %}

  function getPopupText(feature) {
    return feature.properties["Name"] + ": "
      + feature.properties["information-link"];
  }

  function onEachFeature(feature, layer) {
    if (!feature.properties) {
      return;
    }

    if (feature.properties["information-link"] && feature.properties["Name"]) {
      layer.bindPopup(getPopupText(feature));
    }

    layer.setStyle({
      color: feature.properties["stroke"],
      fillColor: feature.properties["fill"],
      fillOpacity: feature.properties["fill-opacity"],
      weight: feature.properties["stroke-width"],
      opacity: feature.properties["opacity"],
    });
  }

  function clickSearchLocation(e) {
    var foundLayers = leafletPip.pointInLayer(e.latlng, geojsonLayer);

    foundLayers.forEach(function(layer) {
      layer.fire("click", {
        latlng: e.latlng,
      });
    });
  }

  function photonClick(e) { 
    this.map.setView([e.geometry.coordinates[1], e.geometry.coordinates[0]], 16);
    var maybe_latlong = L.latLng(
      [e["geometry"]["coordinates"][1],
       e["geometry"]["coordinates"][0]
       ]); var foundLayers =
    leafletPip.pointInLayer(e["geometry"]["coordinates"], geojsonLayer);

    foundLayers.forEach(function(layer) {
      layer.fire("click", {
        latlng: maybe_latlong,
      });
    });
  } 


  mapRoot.hidden = false;
  mapRoot.setAttribute("role", "region");
  mapRoot.setAttribute("aria-label", "Interactive map of Waterloo Region wards");

  var attrib = 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
  var map = new L.Map("map", {
    zoom: 10,
    center: new L.latLng([{{ site.map.center | join: ',' }}]),
    scrollWheelZoom: false,
    zoomControl: false,
  });

  var zoomControl = L.control.zoom({
    position: 'topright',
  });
  zoomControl.addTo(map);

  document.getElementById("map").setAttribute("role", "region");
  document.getElementById("map").setAttribute(
    "aria-label",
    "Interactive map of Waterloo Region wards",
  );

  var baseLayer = new L.TileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    { attribution: attrib },
  );
  var response = await fetch(baseUrl + "/assets/data/WardBoundaries.geojson");
  var data = await response.json();
  var geojson = L.geoJson(data, {
    onEachFeature: onEachFeature,
  });

  geojsonLayer = geojson;

  {% assign bboxarray = site.map.bbox | join: ',' %}

  {% if site.enable-map-search-nominatim %}
      var searchControl = new L.Control.Search({
        url:
        "https://nominatim.openstreetmap.org/search?format=json&countrycodes=ca&viewbox={{ bboxarray }}&bounded=1&q={s}",
        jsonpParam: "json_callback",
        propertyLoc: ["lat", "lon"],
        propertyName: "display_name",
        marker: false,
        autoCollapse: false,
        collapsed: false,
        initial: true,
        autoType: false,
        delayType: 100,
        container: "map-searchbar",
        zoom: 15,
        firstTipSubmit: true,
        textPlaceholder: "Search by address",
        minLength: 3,
      });
      searchControl.on('search:locationfound', clickSearchLocation);
  {% endif %}


  {% if site.enable-map-search-photon %}
      var searchPhotonControl = new L.control.photon({ 
        url: "https://photon.komoot.io/api/?",
        placeholder: "Type your address",
        minChar: 3,
        includePosition: true,
        bbox: [{{ bboxarray }}],
        lang: "en",
        onSelected: photonClick,
        position: 'topleft',
      });
  {% endif %}


  map.addLayer(baseLayer);
  map.addLayer(geojson);
  {% if site.enable-map-search-nominatim %}
      map.addControl(searchControl);

      var searchInput = document.querySelector("#map-searchbar input");
      if (searchInput) {
          searchInput.setAttribute("aria-label", "Search by address to find your ward");
          searchInput.setAttribute("autocomplete", "street-address");
      }
  {% endif %}

  {% if site.enable-map-search-photon %}
      map.addControl(searchPhotonControl);
  {% endif %}

};

