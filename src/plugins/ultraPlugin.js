var resources = require('./../resources/model');

var model = resources.pi.sensors.ultra;
var pluginName = model.name;
var Gpio = require('pigpio').Gpio;

// The number of microseconds it takes sound to travel 1cm at 20 degrees celcius
const MICROSECDONDS_PER_CM = 1e6 / 34321;
const frequency = 1000;
const trigger = new Gpio(model.gpioOut, { mode: Gpio.OUTPUT });
const echo = new Gpio(model.gpioIn, { mode: Gpio.INPUT, alert: true });
trigger.digitalWrite(0); // Make sure trigger is low


let interval;

const watchHCSR04 = () => {
	let startTick;

	echo.on('alert', (level, tick) => {
		if (level == 1) {
			startTick = tick;
		} else {
			const endTick = tick;
			const diff = (endTick >> 0) - (startTick >> 0); // Unsigned 32 bit arithmetic
			model.value = diff / 2 / MICROSECDONDS_PER_CM;
			console.info('Ultra Proximity: %s', model.value);
		}
	});
};

exports.start = function(params) {
	watchHCSR04();

	interval = setInterval(() => {
		trigger.trigger(10, 1); // Set trigger high for 10 microseconds
	}, frequency); 
};

exports.stop = function() {
	clearInterval(interval)

	console.info('%s plugin stopped!', pluginName);
};
