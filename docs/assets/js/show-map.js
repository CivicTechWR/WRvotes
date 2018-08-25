
/* Show map in new way. */

function onEachFeature(feature, layer) {
    if (feature.properties) { 
        if (feature.properties["information-link"] 
          && feature.properties["Name"]) { 
            var msg = feature.properties["Name"] + ": " 
              + feature.properties["information-link"];
            layer.bindPopup(msg);
        } // end if information link

        layer.setStyle({
            color: feature.properties["stroke"],
            fillColor: feature.properties["fill"],
            fillOpacity: feature.properties["fill-opacity"],
            weight: feature.properties["stroke-width"],
            opacity: feature.properties["opacity"]
        });
    }

} 


var attrib = 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
var map = new L.Map('map', {
    zoom: 10, 
    center: new L.latLng([43.45850, -80.51511]),
    scrollWheelZoom:false,
  });

var baselayer = new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    { attribution: attrib });     //base layer


var searchControl = new L.Control.Search({
    url: 'https://nominatim.openstreetmap.org/search?format=json&countrycodes=ca&viewbox=-80.7907,43.2281,-80.0834,43.6032&bounded=1&q={s}',
    jsonpParam: 'json_callback',
    propertyLoc: ['lat','lon'],
    propertyName: 'display_name',
    marker: false,
    autoCollapse: false,
    collapsed: false,
    autoType: false,
    container: 'map-searchbar',
    zoom: 15,
    minLength: 3
    });

searchControl.on('search_locationfound', function(e) { 
    console.log(e)
    e.layer.openPopup().openOn(map);
});

map.addControl(searchControl);

$.getJSON("./assets/data/WardBoundaries.geojson", function(data) {
    var geojson = L.geoJson(data, {
      onEachFeature: onEachFeature
    });

    // Make a combined layer so the popups will work?
    //geojson.addTo(map);
    L.featureGroup([baseLayer, geojson]).addTo(map);
});
 



