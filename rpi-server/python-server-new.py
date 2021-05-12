from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
import json
import threading
import time
import logging
import cv2
import math
import chalk
import RPi.GPIO as GPIO

"""
	VARIABLES
"""
payload = None
loop_fsr = True
loop_opencv = True
home_cups = 0
away_cups = 0
vs = None

"""
	CONSTANTS
"""
RESET_BOARD = "RESET_BOARD";
START_BOARD = "START_BOARD";
STOP_BOARD = "STOP_BOARD";
FSR = "fsr"
OPEN_CV = "opencv"
WIN = 'WIN';



def client_iot_init():
	"""
		Create client
	"""
	### YOUR CODE HERE
	# Create an IoT Hub client
	CONNECTION_STRING = "HostName=ProjectHub.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=h5EkuDGBCk/H+fEsKnfwT0M0n+HSJ7VGO5J1vMSfmkw="
	client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
	### END CODE
	return client


def shutdown():
	""" 
		Shutdown all runningcode.
	"""
	### YOUR CODE HERE
	GPIO.cleanup()
	vs.release()
	cv2.destroyAllWindows()
	### END CODE


def device_method_listener(client):
	logging.info("--> Thread: device_method_listener()")
	""" 
		Create listener for events.
	"""
	global payload
	while True:
		logging.info("--> Thread: device_method_listener().while()")

		method_request = client.receive_method_request()
		if method_request.name == "scoreBoard":
			try:
				### YOUR CODE HERE
				body = json.loads(method_request.payload)
				payload = body
				### END CODE
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


def sendMqgBallInCupMsg(client, eventType, teamName, score):
	bicEvent = {'eventtype': eventType, 'team': teamName, 'score': score}
	serializedMsg = json.dumps(bicEvent, sort_keys=True, indent=3)
	logging.info(f"--> Main: Sending MSG =>{bicEvent}")
	message = Message(serializedMsg)
	client.send_message(message)



def readadc(SPICS, SPICLK, SPIMOSI, SPIMISO , potentiometer_adc):
    if ((potentiometer_adc > 7) or (potentiometer_adc < 0)):
            return -1
    
    GPIO.output(SPICS, True)
    GPIO.output(SPICLK, False)  # start clock low
    GPIO.output(SPICS, False)     # bring CS low

    commandout = potentiometer_adc
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here

    for i in range(5):
        if (commandout & 0x80):
                GPIO.output(SPIMOSI, True)
        else:
                GPIO.output(SPIMOSI, False)
        commandout <<= 1
        GPIO.output(SPICLK, True)
        GPIO.output(SPICLK, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
            GPIO.output(SPICLK, True)
            GPIO.output(SPICLK, False)
            adcout <<= 1
            if (GPIO.input(SPIMISO)):
                    adcout |= 0x1

    GPIO.output(SPICS, True)
    
    adcout >>= 1       # first bit is 'null' so drop it
    return adcout


def loopFSR(client):
	global away_cups
	global home_cups
	global loop_fsr
	GPIO.setmode(GPIO.BCM)
	last_read = 0
	delay = 0.05
	tolerance = 40
	SPICLK = 18
	SPIMISO = 23
	SPIMOSI = 24
	SPICS = 25
	GPIO.setup(SPIMOSI, GPIO.OUT)
	GPIO.setup(SPIMISO, GPIO.IN)
	GPIO.setup(SPICLK, GPIO.OUT)
	GPIO.setup(SPICS, GPIO.OUT)

	# 10k trim pot connected to adc #0
	potentiometer_adc = 0;
	while loop_fsr:
		pad_value = readadc(SPICS, SPICLK, SPIMOSI, SPIMISO , potentiometer_adc)
		pot_adjust = abs(pad_value - last_read)
		if ( pot_adjust > tolerance ):
			last_read = pad_value
			if pot_adjust <= 300: # 
				# eventType, teamName, score
				logging.info(chalk.green("--> Main.fsr: BIC -------"))
				sendMqgBallInCupMsg(client, "BIC", "HOME", home_cups)
			elif pot_adjust > 300:
				away_cups -= 1
				if away_cups == 0:
					logging.info(chalk.green("--> Main.fsr: WIN -------"))
					sendMqgBallInCupMsg(client, WIN, "AWAY", away_cups)
				else: 
					logging.info(chalk.green("--> Main.fsr: CR -------"))
					sendMqgBallInCupMsg(client, "CR", "AWAY", away_cups)

		time.sleep(delay)



def ballInCup(cupPos, ballPos):
	"""
		https://stackoverflow.com/questions/33490334/check-if-a-circle-is-contained-in-another-circle
	"""
	if (len(cupPos) < 1 or len(ballPos) < 1):
		return False
	cx, cy, cradious = cupPos[0]
	bx, by, bradious = ballPos[0]
	d = math.sqrt( (bx-cx)**2 + (by-cy)**2 )
	if (cradious > (d + bradious)):
		return True;
	else:
		return False;


def loopOpenCV(client):
	global loop_opencv
	global away_cups
	global home_cups
	global vs 
	vs = cv2.VideoCapture(0)
	TIME_THRESHOLD = 2.05
	cupPos = []
	ballPos = []
	t = 200
	time.sleep(2.0)
	start_bic = time.time()
	start_cr = time.time()
	while loop_opencv:
		_, frame = vs.read()
		if frame is None:
			logging.info(f"--> Main: frame=None")
			break
		gray = cv2.cvtColor(src = frame, code = cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(src = gray, 
			ksize = (5, 5), 
			sigmaX = 0)
		(t, binary) = cv2.threshold(src = blur,
			thresh = t, 
			maxval = 255, 
			type = cv2.THRESH_BINARY)
		(contours, _) = cv2.findContours(image = binary, 
			mode = cv2.RETR_TREE,
			method = cv2.CHAIN_APPROX_SIMPLE)

		for (_, c) in enumerate(contours):
			((x1, y1), radius1) = cv2.minEnclosingCircle(c)
			if (170 <= radius1 * 2 <= 280):
				cupPos.insert(0,[x1, y1, radius1])
			if (24 <= radius1 * 2 <= 80):
				ballPos.insert(0,[x1, y1, radius1])

		end_bic = time.time()
		time_elapsed_bic = end_bic - start_bic
		if ballInCup(cupPos, ballPos):
			if time_elapsed_bic > TIME_THRESHOLD:
				logging.info(chalk.green("--> Main.openCV: Ball in cup"))
				# eventType, teamName, score
				sendMqgBallInCupMsg(client, "BIC", "AWAY", 200) 
				start_bic = end_bic;
		end_cr = time.time()
		time_elapsed_cr = end_cr - start_cr
		if len(contours) == 0:
			if time_elapsed_cr > TIME_THRESHOLD:
				logging.info(chalk.green("--> Main.openCV: Cup removal -------"))
				home_cups -= 1
				if home_cups == 0:
					sendMqgBallInCupMsg(client, "CR", "HOME", home_cups) 
				else: 
					sendMqgBallInCupMsg(client, "WIN", "HOME", home_cups) 

				start_cr = end_cr;


		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break
		

def startBoard(client, payload):
	global home_cups 
	global away_cups 
	home_cups = int(payload["homecups"])
	away_cups = int(payload["awaycups"])
	detection_metohd = payload["method"]

	if detection_metohd == FSR:
		loopFSR(client)
	elif detection_metohd == OPEN_CV:
		loopOpenCV(client)


def stopBoard():
	global loop_fsr
	global loop_opencv
	global vs
	loop_fsr = False
	loop_opencv = False
	vs.release()

def resetBoard():
	global loop_fsr
	global loop_opencv
	loop_fsr = True
	loop_opencv = True

def main():
	""" 
		Main running loop
	"""
	### YOUR CODE HERE
	global payload
	client = client_iot_init()
	try:
		# Start a thread to listen
		device_method_thread = threading.Thread(target=device_method_listener, args=(client,))
		device_method_thread.daemon = True
		device_method_thread.start()

		while True:

			if payload == None:
				logging.info("--> Main: Sleeping...")
				time.sleep(0.5)
				continue

			event_type = payload["eventtype"]
			logging.info(f"--> Main: event={event_type}")
			if event_type == RESET_BOARD:
				resetBoard()
				payload = None
			elif event_type == START_BOARD:
				startBoard(client, payload)
			elif event_type == STOP_BOARD:
				stopBoard()
				payload = None

	except KeyboardInterrupt:
		print("")
		logging.info("--> Main: Python server stopping")
		shutdown()

if __name__ == '__main__':
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO, 
			datefmt='%d-%b-%y %H:%M:%S'	) # datefmt="%H:%M:%S"
	logging.info("--> Main: Starting up server")
	logging.info("--> Main: Press Ctrl-C to exit")
	main()