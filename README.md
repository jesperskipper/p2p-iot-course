# Follow the steps below to run:


## Getting the code

To clone the repository run:

```
git clone https://gitlab.au.dk/p2p/iot-project.git
```


Next checkout branch `easypong`:

```
git checkout easypong
```

Now the there is 2 folders `html-dashboard` and `rpi-server`


## HTML dashboard (local)


**Build dashboard**

``` bash
 $ cd html-dashboard/
 $ npm install
 $ npm start 
```

Now go to `http://localhost:5000/`


## Python server (on Rpi)

**Requirements python version**
You need a python version above `3.6` to run code below.

**Build Pi dependicies**

``` bash
 $ cd rpi-server/
 $ pip install azure.iot.device
 $ pip install azure-iothub-device-client
 $ pip install azure
 $ pip install pychalk
 $ pip install cv2
 $ pip install RPi.GPIO
```

To run the server: `python3 python-server-new.py`


**Primary connection String**

`'HostName=ProjectHub.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=h5EkuDGBCk/H+fEsKnfwT0M0n+HSJ7VGO5J1vMSfmkw='`

