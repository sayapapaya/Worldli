(function(){

var API_KEY = "AIzaSyD-oVtT-NbHwFJDJkjKbbe-I4llMFBbXtg";

function findCityName(latitude,longitude) {
	$.ajax({
		url: "https://maps.googleapis.com/maps/api/geocode/json?latlng="+latitude+","+longitude+"&key="+API_KEY,
		type: "GET",
		dataType: "json",
		success: function (result) {
			if (result.status == "OK") {
				for (i in result["results"]) {
					if (result["results"][i]["types"][0] == "locality")
						$("#location")[0].value = result["results"][i]["formatted_address"];
				}
			}
		},
		error: function(xhr, errmsg, err) {
	      console.log(xhr.status + ": " + xhr.responseText);
	    }
	});
}	

if (navigator.geolocation) {
	navigator.geolocation.getCurrentPosition(function(position) {
		findCityName(position.coords.latitude, position.coords.longitude);
	});
}

})();