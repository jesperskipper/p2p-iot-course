const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');
const EventHubReader = require('./event-hub-reader.js');
const callDIrectMethod = require('./call-device-application');


// const iotHubConnectionString = process.env.IotHubConnectionString;
const iotHubConnectionString =
	'HostName=ProjectHub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=0SGEzaMTzALTffnZTEPWtuSN7/D7WTryuQhRvnR1Hzc=';
// const iotHubConnectionString = "HostName=projectp2phub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=Deu0nsz3fRe4ahns+PXeIcAH5XkZrcws6vEN+SqA1G8=";
// const iotHubConnectionString = "HostName=projectp2phub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=Deu0nsz3fRe4ahns+PXeIcAH5XkZrcws6vEN+SqA1G8=";

// const eventHubConsumerGroup = process.env.EventHubConsumerGroup;
const eventHubConsumerGroup = 'ProjectConsumerGroup';
// const eventHubConsumerGroup = 'consumerGroupProject';

// Redirect requests to the public subdirectory to the root
const app = express();
// app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public-dashboard')));
app.get('/', function(req, res) {
	res.redirect('/dashboard.html');
});

// app.use((req, res /* , next */) => {
// 	res.redirect('/');
// });

const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

//Server to view
wss.broadcast = (data) => {
	wss.clients.forEach((client) => {
		if (client.readyState === WebSocket.OPEN) {
			try {
				console.log(`Broadcasting data ${data}`);
				client.send(data);
			} catch (e) {
				console.error(e);
			}
		}
	});
};

//Connection between view and server
wss.on('connection', function(w) {
	//Mesage from view to server
	w.on('message', function(msg) {
		console.log('message from client');
		var data = JSON.parse(msg);
		console.log('--> w.on("message").msg: ', data);

		var eventType = data.eventtype;
		var deviceId = (data.deviceId == null ? "MyPythonDevice": data.deviceId);

		
		
		var methodParams = {
			methodName: 'scoreBoard',
			payload: JSON.stringify(data), // value to send to IOT device.
			responseTimeoutInSeconds: 30
		};
		// change led on PI by calling DirectMethoding.
		// Server to hub
		callDIrectMethod.callDevice(deviceId, methodParams);
	});

	w.on('close', function() {
		console.log('closing connection');
	});
});

var port = normalizePort(process.env.PORT || '5000');

server.listen(port, () => {
	console.log('Listening on %d.', server.address().port);
	console.log('Adress is http://localhost:' + port);
});

const eventHubReader = new EventHubReader(iotHubConnectionString, eventHubConsumerGroup);

(async () => {
	await eventHubReader.startReadMessage((message, date, deviceId) => {
		try {
			const payload = {
				IotData: message,
				MessageDate: date || Date.now().toISOString(),
				DeviceId: deviceId
			};

			wss.broadcast(JSON.stringify(payload));
		} catch (err) {
			console.error('Error broadcasting: [%s] from [%s].', err, message);
		}
	});
})().catch();

function normalizePort(val) {
	var port = parseInt(val, 10);

	if (isNaN(port)) {
		// named pipe
		return val;
	}

	if (port >= 0) {
		// port number
		return port;
	}

	return false;
}
