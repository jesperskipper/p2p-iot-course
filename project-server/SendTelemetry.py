# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import threading
import json

# Using the Python Device SDK for IoT Hub: https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI: az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=ProjectHub.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=h5EkuDGBCk/H+fEsKnfwT0M0n+HSJ7VGO5J1vMSfmkw="

START_AMOUNT = 6
EVENT_TYPE = None

# Define the JSON message to send to IoT Hub.
HOME_NAME = "HOME"
AWAY_NAME = "AWAY"
BIC = "BIC"
WIN = "WIN"
CR = "CR"

HOME_CUPS = START_AMOUNT
AWAY_CUPS = START_AMOUNT
MSG_TXT = '{{"Home cups remaining": {home_cup},"Away cups remaining": {away_cup}}}'
MSG_WINNER = '{{"The winner is": {winner}}}'


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client


def device_method_listener(device_client):
    global EVENT_TYPE
    while True:
        method_request = device_client.receive_method_request()
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )
        if method_request.name == "resetBoard": #TODO: The name of the direct method
            try:
                body = json.loads(method_request.payload)
                print(":::::", body["eventtype"])
                # HOME_NAME = method_request.payload.home #TODO: PAYLOAD must contain this
                # AWAY_NAME = method_request.payload.away # TODO: PAYLOAD must contain this
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                # FIXME: Here is the method you should do!
                print("RESET BOARD!!!!")
                response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
                response_status = 200
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        device_client.send_method_response(method_response)



def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        
        home_cups = HOME_CUPS
        away_cups = AWAY_CUPS
        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        # Start a thread to listen 
        device_method_thread = threading.Thread(target=device_method_listener, args=(client,))
        device_method_thread.daemon = True
        device_method_thread.start()



        while True:
            time.sleep(2)
            print("Home team is: ", HOME_NAME)
            print("Away team is: ", AWAY_NAME)
            bicEvent = {}
            crEvent = {}
            winEvent = {}
            # Build the message with simulated telemetry values.
            if (home_cups > away_cups):
                home_cups = home_cups-1
                bicEvent = {'eventtype': BIC, 'team': HOME_NAME, 'score': home_cups}
            else:
                away_cups = away_cups-1
                bicEvent = {'eventtype': BIC, 'team': AWAY_NAME, 'score': away_cups}

            serializedMsg = json.dumps(bicEvent, sort_keys=True, indent=3)
            # msg_txt_formatted = MSG_TXT.format(home_cup=home_cups, away_cup=away_cups)
            # print("MSG:", msg_txt_formatted)
            # print("SERI:", serializedMsg)
            message = Message(serializedMsg)

            # Send the message.
            print("Sending message: {}".format(message))
            client.send_message(message)
            print("Message successfully sent")

            if (home_cups % 2 == 0):
                crEvent = {'eventtype': CR, 'team': HOME_NAME, 'score': home_cups}
                serializedMsg = json.dumps(crEvent, sort_keys=True, indent=3)
                message = Message(serializedMsg)
                client.send_message(message)
            elif (away_cups % 2 == 0):
                crEvent = {'eventtype': CR, 'team': AWAY_NAME, 'score': away_cups}
                serializedMsg = json.dumps(crEvent, sort_keys=True, indent=3)
                message = Message(serializedMsg)
                client.send_message(message)

            if home_cups == 0 or away_cups == 0:
                if home_cups == 0:
                    winner = HOME_NAME
                else:
                    winner = AWAY_NAME

                winEvent = {'eventtype': WIN, 'team': winner}
                serializedMsg = json.dumps(winEvent, sort_keys=True, indent=3)
                # msg_winner_formatted = MSG_WINNER.format(winner=winner)
                winner_msg = Message(serializedMsg)
                client.send_message(winner_msg)
                print("Sending message: {}".format(winner_msg))
                print("Message successfully sent")
                break

            time.sleep(10)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")


if __name__ == '__main__':
    print("IoT Hub: EASYPONG")
    print("Press Ctrl-C to exit")
    iothub_client_telemetry_sample_run()
