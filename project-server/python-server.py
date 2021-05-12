
import argparse
from sendMqttMsg import MqttMSG as MqttMSg
from detecterOpenCV import DetectOpenCV as DetectOpenCV
from detecterFsr import DetectFSR as DetectFSR
import json
import threading
import time

FSR = "FSR"
OPENCV = "openCV"
RESET_BOARD = "RESET_BOARD";
START_BOARD = "START_BOARD";
STOP_BOARD = "STOP_BOARD";

iot_hub_client = None 
mqtt_client = None
open_cv = None 
fsr_sensor = None 

def callBackSendBallInCupMsg(eventType, teamName, score):
        # print("TEST: ", teamName)
        bicEvent = {'eventtype': eventType, 'team': teamName, 'score': score}
        serializedMsg = json.dumps(bicEvent, sort_keys=True, indent=3)
        mqtt_client.iothub_client_send_msg(iot_hub_client, serializedMsg)
        
    

loop_thread = None

def main_loop(method):
    

    def listenCallBack(body):
        print("-->", body)
        global loop_thread
        
        event_type = body["eventtype"]
        if event_type == RESET_BOARD:
            a = 1
            print("reset board -------------")
        elif event_type == START_BOARD:
            if (method == FSR):
                loop_thread = threading.Thread(target=fsr_sensor.runMainLoop, args=(callBackSendBallInCupMsg,))
                loop_thread.daemon = True
                loop_thread.start()
                # fsr_sensor.runMainLoop(callBackSendBallInCupMsg)
            elif method == OPENCV:
                # loop_thread = threading.Thread(target=fsr_sensor.runMainLoop, args=(callBackSendBallInCupMsg,))
                # loop_thread.daemon = True
                open_cv.runMainLoop(callBackSendBallInCupMsg)
            else:
                print(f"Problem method not able to handle")
            
        elif event_type == STOP_BOARD:
            if (method == FSR):
                print("STOP BOARD --- FSR")
                loop_thread.join()
                # fsr_sensor.stopMainLoop()
            elif method == OPENCV:
                open_cv.stopMainLoop()
            else:
                print(f"Problem method not able to handle")
        else:
            print(f"Someting went wrong. Unable to handle {event_type}")

    
    mqtt_client.start_listen(iot_hub_client, listenCallBack)

    # Dummy loop to keep server running
    i = 0
    while True:
        event = None
        event = mqtt_client.get_event_type()
        print(f"Event: epoc_{i} := {event}")
        time.sleep(0.5)
        i += 1
        if event == None:
            continue


if __name__ == '__main__':
    mqtt_client = MqttMSg()
    open_cv = DetectOpenCV()
    fsr_sensor = DetectFSR()
    iot_hub_client = mqtt_client.iothub_client_init()
    print("Starting up server")
    print("Press Ctrl-C to exit")
    parser = argparse.ArgumentParser(description='Python Pi server!')
    parser.add_argument("--t", choices=[FSR, OPENCV], default=FSR, type=str, help="Run with openCV or FSR")
    args = parser.parse_args()
    chosen_method = args.t
    
    try:
        main_loop(method=chosen_method)

    except KeyboardInterrupt:
        print("Stopping python server")
        open_cv.shutdown()
        fsr_sensor.shutdown()
    
    
