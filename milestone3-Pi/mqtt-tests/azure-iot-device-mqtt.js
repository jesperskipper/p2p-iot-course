var clientFromConnectionString = require('azure-iot-device-mqtt').clientFromConnectionString;
var Message = require('azure-iot-device').Message;

// var connectionString = '[IoT Hub device connection string]';
// var connectionString = 'HostName=Alfa-P2P.azure-devices.net;DeviceId=iot-p2p-device;SharedAccessKeyName=service;SharedAccessKey=LvaAPcY+kamALHK3mNVlsE4h+EirHaBNrYAC+YIZrUI=';
var connectionString = 'HostName=Alfa-P2P.azure-devices.net;DeviceId=iot-p2p-device;SharedAccessKey=ORlp2abiU1HZJLq14IajCOn3Y5YygZFOdot2Q1AwJSA=';

var client = clientFromConnectionString(connectionString);

var connectCallback = function(err) {
	if (err) {
		console.error('Could not connect: ' + err);
	} else {
        console.log('Client connected');
        
        var data = JSON.stringify({
            temperature: 10,
            humidity: 65,
            ultra: 200,
            blinkingLed: false,
            led1: 0,
            led2: 1
        });
        // var message = new Message('some data from my device');
        var message = new Message(data);
        
		client.sendEvent(message, function(err) {
			if (err) console.log(err.toString());
		});

		client.on('message', function(msg) {
			console.log(msg);
			client.complete(msg, function() {
				console.log('completed');
			});
		});
	}
};

client.open(connectCallback);
