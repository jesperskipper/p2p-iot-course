// var raspi = require('raspi-io');
//var five = require('johnny-five');

const Raspi = require('raspi-io').RaspiIO;
const five = require('johnny-five');
var board = new five.Board({
	io: new Raspi({
		includePins: [ 'GPIO18', 'GPIO23', 'GPIO24', 'GPIO24', '3.3V' ]
	})
});

board.on('ready', function() {
	// Do work here

	fsr = new five.Sensor({
		freq: 25
	});

	fsr.on('data', (data) => {
		// set the led's brightness based on force
		// applied to force sensitive resistor
		console.log('data', data);
	});
});
