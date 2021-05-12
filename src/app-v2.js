const express = require('express');
var app = express();
var path = require('path');
var bodyParser = require('body-parser');
const PORT = 8080;

var led1 = require('./routes/led1');
var ultra1 = require('./routes/ultra1');
var temp_hum1 = require('./routes/temp-hum1');



app.use(bodyParser.json());


// viewed at http://localhost:8080
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/views/index.html'));
});

app.use('/api/led', led1);
app.use('/api/ultra', ultra1);
app.use('/api/temp-hum', temp_hum1);


app.listen(PORT, () => console.log(`Server listening on port ${PORT}`));
