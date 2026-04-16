window.WRVotesInitMap = async function(baseUrl) {
  var geojsonLayer = null;
  var mapRoot = document.getElementById("map");
  var searchRoot = document.getElementById("map-searchbar");

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

  searchRoot.hidden = false;
  mapRoot.hidden = false;
  mapRoot.setAttribute("role", "region");
  mapRoot.setAttribute("aria-label", "Interactive map of Waterloo Region wards");

  var attrib = 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
  var map = new L.Map("map", {
    zoom: 10,
    center: new L.latLng([43.45850, -80.51511]),
    scrollWheelZoom: false,
  });

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

  var searchControl = new L.Control.Search({
    url: "https://nominatim.openstreetmap.org/search?format=json&countrycodes=ca&viewbox=-80.7907,43.2281,-80.0834,43.6032&bounded=1&q={s}",
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

  searchControl.on("search:locationfound", function(e) {
    var foundLayers = leafletPip.pointInLayer(e.latlng, geojsonLayer);

    foundLayers.forEach(function(layer) {
      layer.fire("click", {
        latlng: e.latlng,
      });
    });
  });

  map.addLayer(baseLayer);
  map.addLayer(geojson);
  map.addControl(searchControl);
};

