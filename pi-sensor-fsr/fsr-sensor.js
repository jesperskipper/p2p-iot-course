var five = require('johnny-five'),
	fsr;
	// led;

new five.Board().on('ready', function() {
	// Create a new `fsr` hardware instance.
	fsr = new five.Sensor({
		pin: 'A0',
		freq: 25
	});

	// led = new five.Led(9);

	// Scale the sensor's value to the LED's brightness range
	fsr.on('data', (data) => {
		// set the led's brightness based on force
		// applied to force sensitive resistor

		console.log("FSR: ", data)

		led.brightness(this.scaled);
	});
});
