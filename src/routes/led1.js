var express = require('express');
var router = express.Router();

// load LED libs
const Gpio = require('onoff').Gpio 
const led = new Gpio(4, 'out') 

// LED
let interval;
let value;

interval = setInterval(() => {
	value = (led.readSync() + 1) % 2; 
	led.write(value, () => {
		console.log('Changed LED state to: ' + value);
	});
}, 2000);



router.get('/', (req, res) => {
    res.json({led: value});
});

process.on('SIGINT', () => {
    clearInterval(interval)
    led.writeSync(0)
    led.unexport()
    console.log('Bye, bye!')
    process.exit()
})

module.exports = router;