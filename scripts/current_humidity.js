// load current humidity values pushed from pi every ten mins											
var humid1 =Papa.parse("humidity_basement_latest_value.csv", {
	download: true,
	complete: function(results) {
		var str2 = "%"
		document.getElementById("live-humid").innerHTML = results.data[1][1].concat(str2); 		
	}
});
// load current temperature values pushed from pi every ten mins											

var temp1 =Papa.parse("temperature_basement_latest_value.csv", {
	download: true,
	complete: function(results) {
		var str1 = " o"
		var str1a = str1.sup()
		var str2 = "C"
		var str3 = str1a.concat(str2)
		document.getElementById("live-temp").innerHTML = results.data[1][1].concat(str3); 		
	}
});
// load external conditions pushed from pi every hour after being called from api											
var humid_out =Papa.parse("current_external_conditions.csv", {
	download: true,
	complete: function(results) {
		
		var str2a = "%"
		document.getElementById("outside-humid").innerHTML = results.data[1][3].concat(str2a); 
		var str1 = " o"
		var str1a = str1.sup()
		var str2 = "C"
		var str3 = str1a.concat(str2)
		document.getElementById("outside-temp").innerHTML = results.data[1][4].concat(str3); 	
		
	}
});

// load text descibing whether it is warmer and more humid outside
var humid_out =Papa.parse("compare_conditions.csv", {
	download: true,
	complete: function(results) {
		console.log
		document.getElementById("compare-temp").innerHTML = results.data[1][2]; 	
		document.getElementById("compare-humid").innerHTML = results.data[1][3]; 	

	}
});
