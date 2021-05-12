'use strict';

var connectionString = 'HostName=Alfa-P2P.azure-devices.net;DeviceId=iot-p2p-device;SharedAccessKey=ORlp2abiU1HZJLq14IajCOn3Y5YygZFOdot2Q1AwJSA=';
var Mqtt = require('azure-iot-device-mqtt').Mqtt;
var DeviceClient = require('azure-iot-device').Client
var client = DeviceClient.fromConnectionString(connectionString, Mqtt);
var blinkledPlugin = require('./src/plugins/blinkingled');
var ledsPlugin = require('./src/plugins/ledsPlugin');
var tempHumPlugin = require('./src/plugins/temp-humPlugin');
var ultraPlugin = require('./src/plugins/ultraPlugin');
var mqttMessage = require('./message-service/mqtt-message');
var changeLedState = require('./directcalls/change-led-state')
var led1 = new ledsPlugin.Setup('1');
var led2 = new ledsPlugin.Setup('2');


// Start plugins
led1.start();
led2.start();
ultraPlugin.start();
tempHumPlugin.start();
blinkledPlugin.start();
mqttMessage.start(client);


// Set up the handler
client.onDeviceMethod('SetLedState', changeLedState.onSetLedState);


process.on('SIGINT', () => {
    // #F
    mqttMessage.stop();
    led1.stop();
    led2.stop();
    ultraPlugin.stop();
    tempHumPlugin.stop();
    blinkledPlugin.stop();
    console.log('Stopped all running plugins and stopped interval! Bye for now!');
    process.exit();
});
