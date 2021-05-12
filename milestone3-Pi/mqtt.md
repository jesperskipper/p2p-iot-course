## Video
- https://www.youtube.com/watch?v=WmKAWOVnwjE


## Cloud:
- https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-live-data-visualization-in-web-apps
- webConsumer (consumergroupname)
- 
```
jesper@Azure:~$ az iot hub consumer-group create --hub-name Alfa-P2P --name webConsumer
{
  "etag": null,
  "id": "/subscriptions/ff0a3f62-a3c9-4f73-87c2-d0928656787e/resourceGroups/P2P-project/providers/Microsoft.Devices/IotHubs/Alfa-P2P/eventHubEndpoints/events/ConsumerGroups/webConsumer",
  "name": "webConsumer",
  "properties": {
    "created": "Sun, 22 Sep 2019 06:49:28 GMT"
  },
  "resourceGroup": "P2P-project",
  "type": "Microsoft.Devices/IotHubs/EventHubEndpoints/ConsumerGroups"
}
```

- Get connection string
```
jesper@Azure:~$ az iot hub show-connection-string --hub-name Alfa-P2P --policy-name service
{
  "connectionString": "HostName=Alfa-P2P.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=LvaAPcY+kamALHK3mNVlsE4h+EirHaBNrYAC+YIZrUI="
}
```

- https://docs.microsoft.com/en-us/azure/iot-hub/quickstart-control-device-node
- 


## Export functions:
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/export


## Tables:
- https://getbootstrap.com/docs/4.0/content/tables/
- 

## Webscokets
- https://blog.revathskumar.com/2015/08/websockets-simple-client-and-server.html
- https://www.tutorialspoint.com/html5/html5_websocket.htm

## Express
- https://expressjs.com/en/starter/basic-routing.html

## Javascript
- https://stackoverflow.com/questions/5515310/is-there-a-standard-function-to-check-for-null-undefined-or-blank-variables-in
- https://stackoverflow.com/questions/14999927/insert-th-in-thead
- https://stackoverflow.com/questions/21168521/table-fixed-header-and-scrollable-body
- https://mdbootstrap.com/docs/jquery/tables/scroll/
- https://stackoverflow.com/questions/42483320/table-with-fixed-header-and-scrolling-table-body-doesnt-let-tbody-scroll
- https://codepen.io/anon/pen/OpVORa
- https://htmldog.com/guides/javascript/advanced/creatingelements/
- https://stackoverflow.com/questions/11152327/how-to-make-html-table-vertically-scrollable/11152394
- http://www.imaputz.com/cssStuff/bigFourVersion.html
- https://stackoverflow.com/questions/16126357/create-html-table-using-javascript/16126408
- https://stackoverflow.com/questions/3216013/get-the-last-item-in-an-array
- https://stackoverflow.com/questions/9109762/adding-css-class-to-a-dynamically-created-row-using-java-script
-
-
-


## Docker for Cloud component.
- https://nodejs.org/de/docs/guides/nodejs-docker-webapp/
- 

## Azure:
- https://docs.microsoft.com/en-us/learn/modules/deploy-run-container-app-service/4-deploy-web-app

```
1. $ az login
2. $ az acr build --file Dockerfile --registry AlfaP2PIotContainer --image iot-cloud-project .
3. $ 
```

- https://iot-cloud-webapp.azurewebsites.net (web app)
- https://docs.microsoft.com/en-us/learn/modules/deploy-run-container-app-service/7-exercise-update-web-app?pivots=javascript
- https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-apt?view=azure-cli-latest
- https://code.visualstudio.com/tutorials/docker-extension/deploy-container
- https://docs.microsoft.com/en-us/azure/iot-hub/quickstart-control-device-node
- https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-raspberry-pi-kit-node-get-started
-