var WebSocketServer = require('ws').Server,
	resources = require('../../src/resources/model');

exports.listen = function(server) {
	var wss = new WebSocketServer({ server: server });
	console.info('WebSocket server started...');
	wss.on('connection', function(ws, req) { // REMOVE: , req 
		//var url = ws.upgradeReq.url; // LOCAL MODE!
		var url = req.url; // DOCKER MODE!
		console.info('URL', url);

		let pathPrefix = url.slice(1);

		console.info("pathprefix: ", pathPrefix);
		try {
			resources.observe((changes) => {
				changes.forEach((change) => {
					if (change.type === 'update' && change.path.join('/').startsWith(pathPrefix)){
						console.info(`${pathPrefix} changed to ${change.object.value}`);
						ws.send(JSON.stringify(changes[0].object), function() {});
					}
				});
			});
		} catch (e) {
			
		}
	});
};
