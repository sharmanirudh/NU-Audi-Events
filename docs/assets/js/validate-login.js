var GITHUB_DOMAIN = "nu-audi-events.anirudhsharma.in";
console.log("Validate js");
var API_DOMAIN = "https://nu-audi-events.herokuapp.com";
if (Cookies.get('NU-Audi-Events') == undefined) {
	console.log("1");
	console.log("window.location   " + window.location);
	console.log(GITHUB_DOMAIN + "/login.html");
	console.log(GITHUB_DOMAIN + "/");
	console.log(window.location != GITHUB_DOMAIN + "/login.html" || window.location != GITHUB_DOMAIN + "/");
	debug();
	// if (window.location != GITHUB_DOMAIN + "/login.html" || window.location != GITHUB_DOMAIN + "/") {
		console.log("2");
		window.location = "./login.html";
	// }
}
else {
	console.log(Cookies.get());
	var url = API_DOMAIN + '/validate-cookie';
	var params = 'value=' + Cookies.get()["NU-Audi-Events"];
	var request = null;
    if (window.XMLHttpRequest) {
        request = new XMLHttpRequest();
     } else {
        request = new ActiveXObject("Microsoft.XMLHTTP");
    }
	request.open('POST', url, true);
	request.responseType = 'text';
	request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	request.onload = function() {
		var response = JSON.parse(request.responseText);
		console.log(window.location);
		console.log(response);
		console.log(response["text"]);
		if (response["text"].localeCompare("Valid cookie.") == 0) {
			console.log("Valid Response on comparison");
			if (window.location.href == GITHUB_DOMAIN + "/" || window.location.href == GITHUB_DOMAIN + "/login.html")
				window.location = "./index.html";
		}
		else {
			console.log("Invalid response on comparison");
			Cookies.remove("NU-Audi-Events");
			window.location = "./login.html";
		}
	}
	request.send(params);
}