var express = require('express'),
    path = require('path'),
    router = express.Router();

// ROOT 
//// PATH: http://raspberrypi.local:8080/ui/
router.use('/', express.static(path.join(__dirname, '../..',  '/src/public-views/ui')));



// SENSORS
//// PATH: http://raspberrypi.local:8080/ui/sensors
router.use('/sensors', express.static(path.join(__dirname, '../..',  '/src/public-views/sensors')));
//// PATH: http://raspberrypi.local:8080/ui/sensors/[humidity, temperature, ultra, blinkingLed]
router.use('/sensors' + '/:sensor', express.static(path.join(__dirname, '../..',  '/src/public-views/sensor')));



// actuators
//// PATH: http://raspberrypi.local:8080/ui/actuators
router.use('/actuators', express.static(path.join(__dirname, '../..',  '/src/public-views/actuators')));
//// PATH: http://raspberrypi.local:8080/ui/actuators/[1, 2]
router.use('/actuators/leds' + '/:actuator', express.static(path.join(__dirname, '../..',  '/src/public-views/actuator')));




module.exports = router;




// router.route('/sensors').get(function(req, res) {
// 	res.sendFile(path.join(__dirname, '../..', '/src/public-views/sensors.html'));
// });

// router.route('/sensors' + '/:id').get(function(req, res) {
// 	res.sendFile(path.join(__dirname, '../..', '/src/public-views/sensor.html'));
// });

// router.route('/').get(function (req, res, next) {
//     req.result = resources.pi.sensors;
//     next();
// });

// router.route('/').get(function(req, res) {
// 	res.sendFile(path.join(__dirname, '../..', '/src/public-views/ui.html'));
// });

