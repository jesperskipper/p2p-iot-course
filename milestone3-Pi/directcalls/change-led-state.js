'use strict';
const chalk = require('chalk');
var resources = require('./../src/resources/model');

// Function to handle the ledstate direct method call from IoT hub
exports.onSetLedState = function(request, response) {
	// Function to send a direct method reponse to your IoT hub.
	function directMethodResponse(err) {
		if (err) {
			console.error(chalk.red('An error ocurred when sending a method response:\n' + err.toString()));
		} else {
			console.log(chalk.green("Response to method '" + request.methodName + "' sent successfully."));
		}
	}

	console.log(chalk.blue('onSetLedState() method called. Received payload:'));
	console.log(chalk.blue("<--", request.payload));

	// Check that a numeric value was passed as a parameter
	if (!request.payload) {
		console.log(chalk.red('Invalid interval response received in payload'));
		// Report failure back to your hub.
		response.send(400, 'Invalid direct method parameter: ' + request.payload, directMethodResponse);
	} else {
		var body = JSON.parse(request.payload);
		resources.pi.actuators.leds[body.ledNumber].value = body.value;
		
		// Report success back to your hub.
		response.send(200, 'Led state set to: ' + request.payload, directMethodResponse);
	}
};


