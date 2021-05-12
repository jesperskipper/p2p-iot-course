# Follow the steps below to run:


## Getting the code

To clone the repository run:

```
git clone https://gitlab.au.dk/p2p/iot-project.git
```


Next checkout branch `milestone3`:

```
git checkout milestone3
```

Now the code is ready to run either manually or using docker.



# Milestone 3

## Cloud 

### WebApp

- https://iot-cloud-webapp.azurewebsites.net/

**Build web app**

``` bash
 $ cd milestone3-Cloud/
 # Locally
 $ npm install
 $ npm start
 # locally docker
 $ docker build -t fancy-pants/cloud-iot-assignment . 
 $ docker run -p -d 5000:5000 fancy-pants/cloud-iot-assignment:latest 
 # to cloud replace "AlfaP2PIotContainer" with your registry
 $ az acr build --file Dockerfile --registry AlfaP2PIotContainer --image iot-cloud-project . 
```

## Pi

### Pi-MQTT-Server


**Build Pi server**

``` bash
 $ cd milestone3-Pi/
 # Locally
 $ npm install
 $ npm start
 # locally docker
 $ docker build -t fancy-pants/pi-iot-assignment . 
 $ docker run -d --privileged fancy-pants/pi-iot-assignment:latest 
```

## Testing
### Test your Pi 
**Primary connection String**

`'HostName=Alfa-P2P.azure-devices.net;DeviceId=iot-p2p-device-alfa-test;SharedAccessKey=k0k8+e2Bkq9tFNlCBfH4fjFRm5kopZJlMANTOWdq0hY='`

## REST endpoints & possible HTTP
- root-endpoint: `https://iot-cloud-webapp.azurewebsites.net/`
