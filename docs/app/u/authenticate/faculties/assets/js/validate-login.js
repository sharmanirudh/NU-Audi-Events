var GITHUB_DOMAIN = "http://nu-audi-events.anirudhsharma.in";
// var GITHUB_DOMAIN = "localhost:8000/nu-audi";
console.log("Faculty login-alidate.js");
var API_DOMAIN = "https://nu-audi-events.herokuapp.com";
if (Cookies.get('NU-Audi-Events') == undefined) {
	console.log("Cookie undefined");
	if (window.location.href != GITHUB_DOMAIN + "/login.html") {
		console.log("Redirecting to login page");
		window.location = "/login.html";
	}
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
			if (window.location.href == GITHUB_DOMAIN + "/")
				window.location = "./app/u/authenticate/faculties/dashboard.html";
		}
		else {
			Cookies.remove("NU-Audi-Events");
			window.location = "/login.html";
		}
	}
	request.send(params);
}