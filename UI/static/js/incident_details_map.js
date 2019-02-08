let newlocationCoordinates;
sessionStorage.removeItem('showPopUp');

function displayMap(geoCoordinates) {
    var map = L.map("googleMap").setView(geoCoordinates, 17);
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
        console.log(e.latlng);

        if (sessionStorage.getItem('showPopUp') === 'enabled') {

            newlocationCoordinates = [e.latlng.lat, e.latlng.lng];
            marker.setLatLng(e.latlng);

        }
    }


    map.on('click', onMapClick);

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


