
var resources = require('./../src/resources/model');
var Message = require('azure-iot-device').Message;

var intervalLoop = null;
var client = null;

exports.start = function(cli) {
    client = cli;
    // Create a message and send it to the IoT hub, initially every second.
    intervalLoop = setInterval(sendMessage, 15000); //TODO: change to 15000 according to subscription on Azure.
};

// Send a telemetry message to your hub
function sendMessage() {
    // Sensors
    var temperature = resources.pi.sensors.temperature.value;
    var humidity = resources.pi.sensors.humidity.value;
    var ultra = resources.pi.sensors.ultra.value;
    var blinkingled = resources.pi.sensors.blinkingLed.value;

    // Actuators
    var led1 = resources.pi.actuators.leds[1].value;
    var led2 = resources.pi.actuators.leds[2].value;

    // Add values to the message body.
    var data = JSON.stringify({
        temperature: temperature,
        humidity: humidity,
        ultra: ultra,
        blinkingLed: blinkingled,
        led1: led1,
        led2: led2
    });
    var message = new Message(data);
    console.log('Sending MQTT message: ' + message.getData());

    // Send the message.
    client.sendEvent(message, function (err) {
        if (err) {
            console.error('send error: ' + err.toString());
        } else {
            console.log('message sent');
        }
    });
}

exports.stop = function() {
    clearInterval(intervalLoop);
    console.info('%s plugin stopped!', "MQTT-messaging-service");
};


