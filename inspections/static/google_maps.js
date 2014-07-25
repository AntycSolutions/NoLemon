<!-- Compatability
var geocoder;
var map;
var markers;
var addresses = [];

function initialize() {
    markers = [];
    geocoder = new google.maps.Geocoder();
    // edmonton,ab
    var latlng = new google.maps.LatLng(53.5333, -113.5000);
    var mapOptions = {
        zoom: 11, // arbitrary
        center: latlng
    }
    map = new google.maps.Map(document.getElementById('map-canvas'),
                              mapOptions);

    for (var i = 0; i < addresses.length; ++i) {
        codeAddress(addresses[i]);
    }

    // let geocode locations load before centering the map
    sleep(1000, centerMap);
}

function centerMap() {
    var fullBounds = new google.maps.LatLngBounds();
    for(var i = 0; i < markers.length; i++) {
        fullBounds.extend(markers[i].position);
    }
    map.fitBounds(fullBounds);

    if(markers.length == 1) {
        var mSum = 0;
        var mZoom = map.getZoom();
        mSum = parseInt(mZoom) - 8;
        map.setZoom(mSum);
    }
}

function codeAddress(address) {
    geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            addMarker(results[0].geometry.location);
        } else {
            alert('Geocode was not successful '
                  + 'for the following reason: ' + status);
        }
    });
}

function addMarker(location) {
    var marker = new google.maps.Marker({
        map: map,
        position: location
    });
    markers.push(marker);
}

function sleep(millis, callback) {
    setTimeout(function() { callback(); }, millis);
}

google.maps.event.addDomListener(window, 'load', initialize);
// End Compatability -->
