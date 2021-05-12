
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
import threading
import json

EVENT_TYPE = None

class MqttMSG(object):
    def __init__(self):
        self.test = "a1"
        # self.CONNECTION_STRING = "HostName=ProjectHub.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=h5EkuDGBCk/H+fEsKnfwT0M0n+HSJ7VGO5J1vMSfmkw="
        self.CONNECTION_STRING = "HostName=projectp2phub.azure-devices.net;DeviceId=MyPythonServer;SharedAccessKey=Zj3KLcCKLMKR2aSW/0lr70/umZY5rhOVYQUWhfkVPQQ="
    
    def iothub_client_init(self):
        # Create an IoT Hub client
        client = IoTHubDeviceClient.create_from_connection_string(self.CONNECTION_STRING)
        return client

    def iothub_client_send_msg(self, client, jsonMsg):

        message = Message(jsonMsg)
        # print("Sending message: {}".format(message))
        client.send_message(message)
        # print("Message successfully sent")

    def start_listen(self, client, callback):
        device_method_thread = threading.Thread(target=self.device_method_listener, args=(client,callback,))
        device_method_thread.daemon = True
        device_method_thread.start()
    
    def device_method_listener(self, client, callback):
        global EVENT_TYPE
        while True:
            method_request = client.receive_method_request()
            print("--> device_method_listener.while()")

            if method_request.name == "scoreBoard":
                try:
                    body = json.loads(method_request.payload)
                    # print(":::::", body["eventtype"])
                    EVENT_TYPE = body["eventtype"]
                    callback(body)
                except ValueError:
                    response_payload = {"Response": "Invalid parameter"}
                    response_status = 400
                else:
                    response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
                    response_status = 200
            else:
                response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
                response_status = 404

            method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
            client.send_method_response(method_response)
    def get_event_type(self):
        return EVENT_TYPE