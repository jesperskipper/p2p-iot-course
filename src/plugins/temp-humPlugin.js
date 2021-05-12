var resources = require('./../resources/model');

var sensor;
var model = resources.pi.sensors;
var pluginName = model.temperature.name + ' & ' + model.humidity.name;

exports.start = function() {
	var sensorDriver = require('node-dht-sensor');
	sensor = {
		initialize: function() {
			return sensorDriver.initialize(22, model.temperature.gpio);
		},
		read: function() {
			var readout = sensorDriver.read();
			model.temperature.value = parseFloat(readout.temperature.toFixed(2));
			model.humidity.value = parseFloat(readout.humidity.toFixed(2));
			console.info('Temperature: %s C, humidity %s %', model.temperature.value, model.humidity.value);

			setTimeout(function() {
				sensor.read();
			}, model.temperature.frequency);
		}
	};
	if (sensor.initialize()) {
		console.info('Hardware %s sensor started!', pluginName);
		sensor.read();
	} else {
		console.warn('Failed to initialize sensor!');
	}
};

exports.stop = function() {
	// sensor.unexport();
	console.info('%s plugin stopped!', pluginName);
};
