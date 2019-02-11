let newlocationCoordinates;
sessionStorage.removeItem('showPopUp');

function displayMap(geoCoordinates) {
    L.mapbox.accessToken = 'pk.eyJ1Ijoia2Fsc21pYyIsImEiOiJjanJ4N3VobmgwaXF0NDluaDZxeDZ0eGx6In0.RLQH5uKvNHuKhYZXURv58A';
    // L.mapbox.accessToken = 'pk.eyJ1Ijoia2Fsc21pYyIsImEiOiJjanJ3dnI2ZzkwZmZtNDRuMWN2Ymxkb3gyIn0.GAIeAW40W9zFy0YKCCb2Yw';
    let map = L.mapbox.map('googleMap', 'mapbox.streets').setView(geoCoordinates, 17)
        .addControl(L.mapbox.geocoderControl('mapbox.places', {
            keepOpen: false,
            autocomplete: true,
        }));


    var circle = L.circle(geoCoordinates, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 20
    }).addTo(map);


    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let marker = new L.marker(geoCoordinates).addTo(map);


    function onMapClick(e) {

        if (sessionStorage.getItem('showPopUp') === 'enabled') {

            newlocationCoordinates = [e.latlng.lat, e.latlng.lng];
            marker.setLatLng(e.latlng);

        }
    }


    map.on('click', onMapClick);
    L.control.fullscreen().addTo(map);
    L.control.locate().addTo(map);


}

L.TiltHandler = L.Handler.extend({
    addHooks: function () {
        L.DomEvent.on(window, 'deviceorientation', this._tilt, this);
    },

    removeHooks: function () {
        L.DomEvent.off(window, 'deviceorientation', this._tilt, this);
    },

    _tilt: function (ev) {
        this._map.panBy(L.point(ev.gamma, ev.beta));
    }
});

L.Map.addInitHook('addHandler', 'tilt', L.TiltHandler);


