const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');
const EventHubReader = require('./scripts/event-hub-reader.js');
const callDIrectMethod = require('./scripts/BackEndApplication');

// const iotHubConnectionString = process.env.IotHubConnectionString;
const iotHubConnectionString = "HostName=Alfa-P2P.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=LvaAPcY+kamALHK3mNVlsE4h+EirHaBNrYAC+YIZrUI=";
// const eventHubConsumerGroup = process.env.EventHubConsumerGroup;
const eventHubConsumerGroup = "webConsumer";

// Redirect requests to the public subdirectory to the root
const app = express();
app.use(express.static(path.join(__dirname, 'public-views')));
app.use((req, res /* , next */) => {
  res.redirect('/');
});


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
// var deviceId = 'iot-p2p-device'; // iot-p2p-device

//Connection between view and server
wss.on('connection', function(w){

  //Mesage from view to server
  w.on('message', function(msg){
    console.log('message from client');
    var data = JSON.parse(msg);
    console.log('--> w.on("message").msg: ', data);

    var deviceId = data.deviceId;
    var methodParams = {
      methodName: 'SetLedState',
      payload: JSON.stringify({ ledNumber: data.ledNumber, value: data.value }), // value to send to IOT device.
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

// 
// listen on port 8080. Like specified in Dockerfile.
// resources.pi.port
// process.env.PORT || '5000'
var port = normalizePort(process.env.PORT || '5000');

server.listen(port, () => {
  console.log('Listening on %d.', server.address().port);
});

const eventHubReader = new EventHubReader(iotHubConnectionString, eventHubConsumerGroup);

(async () => {
  await eventHubReader.startReadMessage((message, date, deviceId) => {
    try {
      const payload = {
        IotData: message,
        MessageDate: date || Date.now().toISOString(),
        DeviceId: deviceId,
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