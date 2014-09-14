<!-- Compatability

/*  To use include:
    <script type="text/javascript"
            src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB-vNlhTCDa-R9HRfEmquZdIXIGmEp_Kuo"></script>
    <script type="text/javascript"
            src="{% static 'js/google_maps.js' %}"></script>

    Contains map:
    <div style="height: 640px; width: 640px" id="map-canvas"></div>

    For each marker:
    <script type="text/javascript">
        addresses.push("{~ Change ~}");
    </script>
 */

var geocoder;
var map;
var markers;
var addresses = [];
var markerTitles = [];
var labelCode = 65;

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
        codeAddress(addresses[i], markerTitles[i]);
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

function codeAddress(address, title) {
    geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            addMarker(results[0].geometry.location, title);
        } else {
            alert('Geocode was not successful '
                  + 'for the following reason: ' + status);
        }
    });
}

function addMarker(location, title) {
    var label = String.fromCharCode(labelCode);
    var marker = new google.maps.Marker({
        map: map,
        position: location,
        title: title
    });
    ++labelCode;
    markers.push(marker);
    marker.setMap(map);
}

function sleep(millis, callback) {
    setTimeout(function() { callback(); }, millis);
}

google.maps.event.addDomListener(window, 'load', initialize);
// End Compatability -->
