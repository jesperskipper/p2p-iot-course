const express = require('express');
const http = require('http');
const path = require('path');
const WebSocket = require('ws');
const cors = require('cors');

// Redirect requests to the public subdirectory to the root
const app = express();

app.use(cors());

app.use(express.static(path.join(__dirname, 'public')));
app.use((req, res /* , next */) => {
	res.redirect('/');
});

const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

var port = normalizePort(process.env.PORT || '5000');

server.listen(port, () => {
	console.log('Listening on %d.', server.address().port);
});

function normalizePort(val) {
	var port = parseInt(val, 10);

	if (isNaN(port)) {
		// named pipe
		return val;
	}

	if (port >= 0) {
		// port number
		return port;
	}

	return false;
}
