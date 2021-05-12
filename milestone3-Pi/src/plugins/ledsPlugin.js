var resources = require('../resources/model');

exports.Setup = function(ledNumber) {
	var model = resources.pi.actuators.leds[ledNumber];
	var pluginName = model.name;
	var Gpio = require('onoff').Gpio;
	var actuator = new Gpio(model.gpio, 'out');

	var config = {
		start: function() {
			observe(actuator, model, pluginName);
			console.info('--> Hardware %s actuator started!', pluginName);
		},
		stop: function() {
			actuator.unexport();
			console.info('%s plugin stopped!', pluginName);
		}
	};

	return config;
};

function observe(actuator, modelParam, plugNameParam) {
	resources.observe((changes) => {
		changes.forEach((change) => {
			// console.info("-->LED= %s, change are = %s", plugNameParam, JSON.stringify(change))
			if (
				change.type === 'update' &&
				modelParam === change.path.slice(0, -1).reduce((obj, i) => obj[i], resources)
			) {
				switchOnOff(actuator, change.value, plugNameParam);
			}
		});
	});
}

function switchOnOff(actuator, value, plugNameParam) {
	actuator.write(value === true ? 1 : 0, function() {
		console.info('Changed value of %s to %s', plugNameParam, value);
	});
}
