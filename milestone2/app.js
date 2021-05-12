var express = require('express');
var path = require('path');
var cors = require('cors');
var wsServer = require('./server/websockets');
var actuatorsRoutes = require('./routes/actuators');
var sensorRoutes = require('./routes/sensors');
var uiRoutes = require('./routes/ui-router');
var blinkledPlugin = require('../src/plugins/blinkingled');
var ledsPlugin = require('../src/plugins/ledsPlugin');
// const led2Plugin = require('./plugins/ledsPlugin');
var tempHumPlugin = require('../src/plugins/temp-humPlugin');
var ultraPlugin = require('../src/plugins/ultraPlugin');
var converter = require('./converting/converter');
var resources = require('../src/resources/model');
var bodyParser = require('body-parser');

var app = express();
var led1 = new ledsPlugin.Setup('1');
var led2 = new ledsPlugin.Setup('2');

// Do not change order!
app.use(bodyParser.json());
app.use(cors());

// viewed at http://localhost:8080
app.get('/', function(req, res) {
	res.sendFile(path.join(__dirname + '/public-views/index.html'));
});
app.get('/pi', function(req, res) {
	res.send('This is the WoT-API-Pi!');
});

// Routes
app.use('/pi/actuators', actuatorsRoutes);
app.use('/pi/sensors', sensorRoutes);
app.use('/ui', uiRoutes);

// Needs to be last in chain.
app.use(converter());


// Start plugins
led1.start();
led2.start();
ultraPlugin.start();
tempHumPlugin.start();
blinkledPlugin.start();

// Start HTTP Server
var server = app.listen(resources.pi.port, function() {
	console.log('HTTP server started...');

	// Websockets server
	wsServer.listen(server);

	console.info('Your WoT Pi is up and running on port %s', resources.pi.port);
});

process.on('SIGINT', () => {
	// #F
	led1.stop();
	led2.stop();
	ultraPlugin.stop();
	tempHumPlugin.stop();
	blinkledPlugin.stop();
	console.log('Stopped all running plugins! Bye for now!');
	process.exit();
});
