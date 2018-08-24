
/* Show map in new way. */

var map = new L.Map('map', {zoom: 9, center: new L.latLng([43.575730,-80.002411]) });
map.addLayer(new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'));     //base layer

map.addControl( new L.Control.Search({
        url: 'https://nominatim.openstreetmap.org/search?format=json&countrycodes=ca&viewbox=-80.7907,43.2281,-80.0834,43.6032&bounded=1&q={s}',
        jsonpParam: 'json_callback',
        propertyName: 'display_name',
        propertyLoc: ['lat','lon'],
        marker: L.circleMarker([0,0],{radius:30}),
        autoCollapse: false,
        collapsed: false,
        autoType: false,
        minLength: 2
}) );

