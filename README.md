# Follow the steps below to run:


## Getting the code

To clone the repository run:

```
git clone https://gitlab.au.dk/p2p/iot-project.git
```


Next checkout branch `milestone2`:

```
git checkout milestone2
```

Now the code is ready to run either manually or using docker.


## Running the application manually

Before running make sure the l.9 in `websockets.js`, i.e DOCKER MODE! has been commented out, just as stated below:
```
var url = ws.upgradeReq.url; // LOCAL MODE!
//var url = req.url; // DOCKER MODE!
```	

The application consists of a single file `src/app.js`. It can be started from
the application directory with the `node` command:

```
$ node src/app.js
```

The `package.json` file is set up to include a `start` script and express + sensor
package dependencies. Scripts provide a more convinient way to start the application
using `npm`:

```
$ npm start
```

Once the code running visit:
```
[ip-of-rasp]/8080
```
From here it is possible to view the states of the components by using the static html.


## Building the docker image

Before running make sure the l.8 in `websockets.js`, i.e LOCAL MODE! has been commented out, just as stated below:
```
//var url = ws.upgradeReq.url; // LOCAL MODE!
var url = req.url; // DOCKER MODE!
```	

To build the image, use `docker build` inside the application directory:

```
$ docker build -t fancy-pants/iot-assignment .
```

**Important**: this must be done on a Raspberry Pi with working internet connection.

### Running the docker image

```
$ docker run -d -p 8080:8080 --privileged fancy-pants/iot-assignment
```

## Inspecting application

- Go to url [raspberrypi.local:8080](http://raspberrypi.local:8080/) or `LOCAL_RASPBERRY_PI_IP` on port `8080`
- `index.html` page should load and you can click on the two entries
1. `/pi` Here you navigate via URL.
2. `/ui` Here you navigate using the provided interactions.


## REST endpoints & possible HTTP
- root-endpoint: `http://raspberrypi.local:8080`

- GET `http://raspberrypi.local:8080`

For `/ui`:
- GET `/ui/sensors`
- GET `/ui/sensors/temperature`
- GET `/ui/sensors/humidity`
- GET `/ui/sensors/ultra`
- GET `/ui/sensors/blinkingLed`
- GET `/ui/actuators`
- GET `/ui/actuators/leds`
- GET `/ui/actuators/leds/{id}`
- PUT `/ui/actuators/leds/{id}`


For `/pi`:
- GET `/pi/sensors`
- GET `/pi/sensors/temperature`
- GET `/pi/sensors/humidity`
- GET `/pi/sensors/ultra`
- GET `/pi/sensors/blinkingLed`
- GET `/pi/actuators`
- GET `/pi/actuators/leds`
- GET `/pi/actuators/leds/{id}`
- PUT `/pi/actuators/leds/{id}`

