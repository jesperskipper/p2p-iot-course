var resources = require('../resources/model');
var pluginName;
var led;
let interval;

exports.start = function() {
	model = resources.pi.sensors.blinkingLed;
	pluginName = model.name;
	var Gpio = require('onoff').Gpio;
	led = new Gpio(model.gpio, 'out');
	console.info('Hardware %s actuator started!', pluginName);
	startInterval();
};

function startInterval() {
	interval = setInterval(() => {
		// #C
		model.value = (led.readSync() + 1) % 2; // #D
		led.write(model.value, () => {
			// #E
			console.log('Blinking LED state changed to: ' + model.value);
		});
	}, 2000);
}


exports.stop = function() {
	clearInterval(interval)
    led.writeSync(0) // #G
    led.unexport()
	console.info('%s plugin stopped!', pluginName);
};