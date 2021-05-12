var express = require('express'),
    router = express.Router(),
    resources = require('./../resources/model');

router.route('/').get(function (req, res, next) {
    req.result = resources.pi.sensors;
    next();
});

router.route('/ultra').get(function (req, res, next) {
    req.result = resources.pi.sensors.ultra;
    next();
});

router.route('/temperature').get(function (req, res, next) {
    req.result = resources.pi.sensors.temperature;
    next();
});

router.route('/humidity').get(function (req, res, next) {
    req.result = resources.pi.sensors.humidity;
    next();
});


router.route('/blinkingLed').get(function (req, res, next) {
    req.result = resources.pi.sensors.blinkingLed;
    next();
});

module.exports = router;