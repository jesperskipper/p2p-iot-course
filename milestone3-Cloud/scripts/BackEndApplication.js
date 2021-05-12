// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

'use strict';

// Using the Azure CLI:
// az iot hub show-connection-string --hub-name {YourIoTHubName} --policy-name service --output table

var Client = require('azure-iothub').Client;

var connectionString =
	'HostName=Alfa-P2P.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=LvaAPcY+kamALHK3mNVlsE4h+EirHaBNrYAC+YIZrUI=';
// Connect to the service-side endpoint on your IoT hub.
var client = Client.fromConnectionString(connectionString);

exports.callDevice = function(deviceId, methodParams) {
	// Call the direct method on your device using the defined parameters.
	client.invokeDeviceMethod(deviceId, methodParams, function(err, result) {
		if (err) {
			console.error("Failed to invoke method '" + methodParams.methodName + "': " + err.message);
		} else {
			console.log('Response from ' + methodParams.methodName + ' on ' + deviceId + ':');
			console.log(JSON.stringify(result, null, 2));
		}
	});
};
