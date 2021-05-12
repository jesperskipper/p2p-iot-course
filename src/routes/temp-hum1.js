var express = require('express');
var router = express.Router();
const sensorLib = require('node-dht-sensor');
sensorLib.initialize(22, 12);


// Temp - Hum
let temperature;
let humidity;
// Read temp + Hum
function read() {
	let readout = sensorLib.read(); 
	temperature = readout.temperature.toFixed(2);
	humidity = readout.humidity.toFixed(2);
	console.log(
		'Temperature: ' +
		temperature +
		'C, ' + 
			'humidity: ' +
			humidity +
			'%'
	);
}

sensorLib.initialize(22, 12); 
const tempHumInterval = setInterval(() => {
	read();
}, 2000);




process.on('SIGINT', () => {
	clearInterval(interval);
	console.log('Bye, bye!');
	process.exit();
});

router.get('/', (req, res) => {
    res.json({temperature: temperature, humidity: humidity});
});



module.exports = router;