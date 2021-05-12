var httpServer = require('./servers/http'),
    wsServer = require('./servers/websockets'),
    resources = require('./resources/model');

// Internal Plugins
var ledsPlugin = require('./plugins/ledsPlugin'),
    ultraPlugin = require('./plugins/ultraPlugin'),
    tempHumPlugin = require('./plugins/temp-humPlugin');

// Internal Plugins for sensors/actuators connected to the PI GPIOs
// If you test this with real sensors do not forget to set simulate to 'false'
ultraPlugin.start({ 'simulate': false, 'frequency': 2000 });
ledsPlugin.start({ 'simulate': false, 'frequency': 10000 });
tempHumPlugin.start({ 'simulate': false, 'frequency': 10000 });

// HTTP Server
var server = httpServer.listen(resources.pi.port, function () {
    console.log('HTTP server started...');

    // Websockets server
    wsServer.listen(server);

    console.info('Your WoT Pi is up and running on port %s', resources.pi.port);
});