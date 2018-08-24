
/* Show map in new way. */

var attrib = 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
var map = new L.Map('map', 
  {zoom: 10, 
  center: new L.latLng([43.418611, -80.472778])
  });
map.addLayer(
  new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    { attribution: attrib }));     //base layer

map.addControl( new L.Control.Search({
        url: 'https://nominatim.openstreetmap.org/search?format=json&countrycodes=ca&viewbox=-80.7907,43.2281,-80.0834,43.6032&bounded=1&q={s}',
        jsonpParam: 'json_callback',
        propertyLoc: ['lat','lon'],
        marker: L.circleMarker([0,0],{radius:30}),
        autoCollapse: false,
        collapsed: false,
        autoType: false,
        container: 'map-searchbar',
        zoom: 15,
        minLength: 10
}) );

//        propertyName: 'display_name',
//        tooltipLimit: 0,
