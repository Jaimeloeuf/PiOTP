'use strict'; // Enforce use of strict verion of JavaScript

// Initialize the current mode that the fan is on.
var mode;

function getMode() {
	fetch('http://localhost/api/fan/mode')
		.then((Response) => {
			if (Response.ok)
				mode = Response.text()
		})
		.catch((err) => {
			console.log(err);
			document.getElementById('err').innerHTML = 'Error trying to read the current fan mode from the server!';
		});
}

function setMode(mode) {
	// Call server to set mode and update site after mode is set



	document.getElementById('fan-cur-mode').innerHTML = "Current mode: " + mode;
	if (mode === 'auto')
		document.getElementById('fan-man-controls').style = "display: hidden;";
	else if (mode === 'man')
		document.getElementById('fan-man-controls').style = "display: show;";
}

function manControl(state) {
	// Call server to set state and update site after state is set

	document.getElementById('fan-cur-state').innerHTML = "Current status of fan: " + state;
}