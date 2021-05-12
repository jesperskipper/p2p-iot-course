from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
import json
import threading
import random
import time
import logging
import cv2
import math
import datetime
import chalk
# import RPi.GPIO as GPIO

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
	CONNECTION_STRING_OLD = "HostName=ProjectHub.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=h5EkuDGBCk/H+fEsKnfwT0M0n+HSJ7VGO5J1vMSfmkw="

	# CONNECTION_STRING = "HostName=projectp2phub.azure-devices.net;DeviceId=MyPythonServer;SharedAccessKey=Zj3KLcCKLMKR2aSW/0lr70/umZY5rhOVYQUWhfkVPQQ="
	CONNECTION_STRING = "HostName=projectp2phub.azure-devices.net;DeviceId=MyPythonServer;SharedAccessKey=Zj3KLcCKLMKR2aSW/0lr70/umZY5rhOVYQUWhfkVPQQ="
	client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING_OLD)
	### END CODE
	return client


def shutdown():
	""" One-in-k encoding of vector to k classes 

		Args:
		vec: numpy array - data to encode
		k: int - number of classes to encode to (0,...,k-1)
	"""
	### YOUR CODE HERE
	# GPIO.cleanup()
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
	# sendingTime = datetime.datetime.now().time()
	event = {'eventtype': eventType, 'team': teamName, 'score': score} #  'time': sendingTime
	serializedMsg = json.dumps(event, sort_keys=True, indent=3)
	logging.info(f"--> Main: Sending MSG =>{event}")
	# logging.info(chalk.red(f"--> Main: Sending MSG current time: {sendingTime}"))
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


def fakeReadadc():
    # 100 BIC
    # 100 CR
    # 200 -||-
    values = [146,189,115,400,92,83,91,98,63,60,78,62,44,54,110,66,109,91,69,226,59,89,67,82,95,62,75,86,56,78,643,201,39,87,81,76,94,92,88,84,241,43,55,27,73,75,84,89,71,175,99,87,104,138,59,67,52,74,124,66,58,97,68,77,38,68,346,74,62,89,37,94,52,99,187,125,86,141,54,147,451,47,52,63,85,61,58,92,97,58,63,87,111,51,86,49,42,88,63,93, 914,1022,1019,933,920,667,714,937,961,988,372,584,759,1023,951,902,541,971,951,562,897,987,578,689,898,872,589,638,617,1022,1023,798,761,987,869,341,936,856,719,926,364,489,364,658,798,918,937,962,872,1020,797,835,976,616,958,963,565,934,923,563,762,916,873,1023,533,889,651,1023,1023,719,583,651,746,364,1022,935,955,958,871,385,617,688,728,981,658,468,473,897,614,589,928,963,871,981,767,319,972,987,731,658, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    sleep_time = 1.05
    time.sleep(sleep_time)
    return random.choice(values)


def loopFSR(client):
	global away_cups
	global home_cups
	global loop_fsr
	# GPIO.setmode(GPIO.BCM)
	last_read = 0
	delay = 0.05
	tolerance = 40
	SPICLK = 18
	SPIMISO = 23
	SPIMOSI = 24
	SPICS = 25
	# GPIO.setup(SPIMOSI, GPIO.OUT)
	# GPIO.setup(SPIMISO, GPIO.IN)
	# GPIO.setup(SPICLK, GPIO.OUT)
	# GPIO.setup(SPICS, GPIO.OUT)

	# 10k trim pot connected to adc #0
	potentiometer_adc = 0;
	while loop_fsr:
		# pad_value = readadc(self.SPICS, self.SPICLK, self.SPIMOSI, self.SPIMISO , potentiometer_adc)
		pad_value = fakeReadadc() # TODO: Change to real
		pot_adjust = abs(pad_value - last_read)
		if ( pot_adjust > tolerance ):
			last_read = pad_value
			if pot_adjust <= 300: # 
				# eventType, teamName, score
				sendMqgBallInCupMsg(client, "BIC", "HOME", home_cups)
			elif pot_adjust > 300:
				away_cups -= 1
				if away_cups == 0:
					sendMqgBallInCupMsg(client, WIN, "AWAY", away_cups)
				else: 
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
	# vs = cv2.VideoCapture("./beertwhitetop.h264")
	vs = cv2.VideoCapture("./final140_0_white_bic_cr.h264")
	cupPos = []
	TIME_THRESHOLD = 2.05
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

		### WE DO NOT DO IT NOW
		# draw contours over original image
		# cv2.drawContours(image = frame, 
		# 	contours = contours, 
		# 	contourIdx = -1, 
		# 	color = (0, 255, 0), 
		# 	thickness = 5)
		# logging.info(f"--> Main.openCV: Num contours = {len(contours)}")
		for (_, c) in enumerate(contours):
			((x1, y1), radius1) = cv2.minEnclosingCircle(c)

			if (170 <= radius1 * 2 <= 280):
				cupPos.insert(0,[x1, y1, radius1])
				# cv2.circle(frame, (int(x1), int(y1)), int(radius1),
				# (138,43,226), thickness=15)

			if (24 <= radius1 * 2 <= 80):
				ballPos.insert(0,[x1, y1, radius1])
				# cv2.circle(frame, (int(x1), int(y1)), int(radius1),
				# (255,127,80), thickness=15)
		end_bic = time.time()
		time_elapsed_bic = end_bic - start_bic
		if ballInCup(cupPos, ballPos):
			if time_elapsed_bic > TIME_THRESHOLD:
				logging.info("--> Main.openCV: Ball in cup")
				# eventType, teamName, score
				sendMqgBallInCupMsg(client, "BIC", "AWAY", 200) 
				start_bic = end_bic;
		end_cr = time.time()
		time_elapsed_cr = end_cr - start_cr
		if len(contours) == 0:
			if time_elapsed_cr > TIME_THRESHOLD:
				logging.info("--> Main.openCV: Cup removal -------")
				home_cups -= 1
				if home_cups == 0:
					sendMqgBallInCupMsg(client, "CR", "HOME", home_cups) 
				else: 
					sendMqgBallInCupMsg(client, "WIN", "HOME", home_cups) 

				start_cr = end_cr;

		# cv2.namedWindow(winname = "output", flags = cv2.WINDOW_NORMAL)
		# cv2.imshow(winname = "output", mat = frame)

		# key = cv2.waitKey(1) & 0xFF

		# # if the 'q' key is pressed, stop the loop
		# if key == ord("q"):
		# 	break
		
		#### Delay for 0.1 seconds ####
		# time.sleep(0.1)
	

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


def fakeToVideo(client):
	time.sleep(3.1)
	i = 0
	while True:
		logging.info("--> Main: Sleeping...")

		## FSR
		if i == 100:
			logging.info(f"--> Main.FSR: {chalk.yellow('BIC')}")
			sendMqgBallInCupMsg(client, "BIC", "AWAY", 6)
			time.sleep(3.2)
			logging.info(f"--> Main.FSR: {chalk.green('CR')}" )
			sendMqgBallInCupMsg(client, "CR", "HOME", 5)

		## OPENCV
		if i == 200:
			logging.info(f"--> Main.openCV: {chalk.yellow('BIC')}")
			sendMqgBallInCupMsg(client, "BIC", "HOME", 6)
			time.sleep(4.3)
			logging.info(f"--> Main.openCV: {chalk.green('CR')}" )
			sendMqgBallInCupMsg(client, "CR", "AWAY", 5)

		i += 1
		time.sleep(0.1)

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

		fakeToVideo(client)
		# while True:

		# 	if payload == None:
		# 		logging.info("--> Main: Sleeping...")
		# 		time.sleep(0.5)
		# 		continue

		# 	event_type = payload["eventtype"]
		# 	logging.info(f"--> Main: event={event_type}")
		# 	if event_type == RESET_BOARD:
		# 		resetBoard()
		# 		payload = None
		# 	elif event_type == START_BOARD:
		# 		startBoard(client, payload)
		# 	elif event_type == STOP_BOARD:
		# 		stopBoard()
		# 		payload = None

	except KeyboardInterrupt:
		print("")
		logging.info("--> Main: Python server stopped")
		shutdown()

if __name__ == '__main__':
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO, 
			datefmt='%d-%b-%y %H:%M:%S'	) # datefmt="%H:%M:%S"
	logging.info("--> Main: Starting up server")
	logging.info("--> Main: Press Ctrl-C to exit")
	# logging.info(chalk.red('foo'))
	main()