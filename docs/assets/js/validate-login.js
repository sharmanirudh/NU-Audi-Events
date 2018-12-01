if (Cookies.get('NU-Audi-Events') == undefined) {
	if (window.location != "https://sharmanirudh.github.io/NU-Audi-Events/login.html")
		window.location = "./login.html";
}
else {
	console.log(Cookies.get());
	var url = 'http://127.0.0.1:5000/validate-cookie';
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
			if (window.location.href == "https://sharmanirudh.github.io/NU-Audi-Events/" || window.location.href == "https://sharmanirudh.github.io/NU-Audi-Events/login.html")
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