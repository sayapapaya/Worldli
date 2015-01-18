$(document).ready(function(){

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
						$("#location-guess")[0].innerHTML = result["results"][i]["formatted_address"];
						$("#location-modal").modal();
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

$('#location')[0].addEventListener('click', function(){
	var text = $('#location')[0].value;
	$.ajax({
		url: "https://maps.googleapis.com/maps/api/place/autocomplete/json?types=regions&input="+text+"&key="+API_KEY,
		type: "GET",
		dataType: "json",
		success: function(result) {
			var predictions = result["predictions"];
			console.log(predictions);
		},
		error: function(xhr, errmsg, err) {
	      console.log(xhr.status + ": " + xhr.responseText);
	    }
	});
});

});