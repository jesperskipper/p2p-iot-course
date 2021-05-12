# Follow the steps below to run:


## Getting the code

To clone the repository run:

```
git clone https://gitlab.au.dk/p2p/iot-project.git
```


Next checkout branch `milestone1`:

```
git checkout milestone1
```

Now the code is ready to run either manually or using docker.


## Running the application manually

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

To build the image, use `docker build` inside the application directory:

```
$ docker build -t fancy-pants/iot-assignment .
```

**Important**: this must be done on a Raspberry Pi with working internet connection.

## Running the docker image

```
$ docker run -d -p 8080:8080 --privileged fancy-pants/iot-assignment
```

## Inspecting application

- Go to url [raspberrypi.local:8080](http://raspberrypi.local:8080/) or `LOCAL_RASPBERRY_PI_IP` on port `8080`
- `index.html` page should load and you can click on the three api entries
1. `/api/led`
2. `/api/utra`
3. `/api/temp-hum`