// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

'use strict';

// Using the Azure CLI:
// az iot hub show-connection-string --hub-name {YourIoTHubName} --policy-name service --output table

var Client = require('azure-iothub').Client;
const chalk = require('chalk');
const error = chalk.bold.red;
const iotHubConnectionString =
	'HostName=ProjectHub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=0SGEzaMTzALTffnZTEPWtuSN7/D7WTryuQhRvnR1Hzc=';
// const iotHubConnectionString =
// 	'HostName=projectp2phub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=Zj3KLcCKLMKR2aSW/0lr70/umZY5rhOVYQUWhfkVPQQ=';

// var connectionString =
// 	'HostName=Alfa-P2P.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=LvaAPcY+kamALHK3mNVlsE4h+EirHaBNrYAC+YIZrUI=';
// Connect to the service-side endpoint on your IoT hub.
var client = Client.fromConnectionString(iotHubConnectionString);

exports.callDevice = function(deviceId, methodParams) {
	// Call the direct method on your device using the defined parameters.
	client.invokeDeviceMethod(deviceId, methodParams, function(err, result) {
		if (err) {
			console.error(error("Failed to invoke method '" + methodParams.methodName + "': " + err.message));
		} else {
			console.log('Response from ' + methodParams.methodName + ' on ' + deviceId + ':');
			console.log(JSON.stringify(result, null, 2));
		}
	});
};
