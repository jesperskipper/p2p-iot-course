import time
import random
# import RPi.GPIO as GPIO

# 10k trim pot connected to adc #0
potentiometer_adc = 0;

class DetectFSR(object):
    def __init__(self):
        self.last_read = 0
        self.delay = 0.05
        self.tolerance = 40
        self.SPICLK = 18
        self.SPIMISO = 23
        self.SPIMOSI = 24
        self.SPICS = 25
        # set up the SPI interface pins
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.SPIMOSI, GPIO.OUT)
        # GPIO.setup(self.SPIMISO, GPIO.IN)
        # GPIO.setup(self.SPICLK, GPIO.OUT)
        # GPIO.setup(self.SPICS, GPIO.OUT)

        self.t = 200
        self.mainLoop = True 
    
    def stopMainLoop(self):
        self.mainLoop = False

    def runMainLoop(self, callback):
        while self.mainLoop:
            # pad_value = readadc(self.SPICS, self.SPICLK, self.SPIMOSI, self.SPIMISO)
            pad_value = fakeReadadc()
            # print("pad_val::::::", pad_value)
            pot_adjust = abs(pad_value - self.last_read)
            if ( pot_adjust > self.tolerance ):
                self.last_read = pad_value
                if pot_adjust <= 300: # 
                    # eventType, teamName, score
                    callback("BIC", "HOME", 1)
                elif pot_adjust > 300:
                    callback("CR", "AWAY", 2)

            time.sleep(self.delay)

    def shutdown(self):
        # GPIO.cleanup()
        a = 10
        



def fakeReadadc():
    # 100 BIC
    # 100 CR
    # 200 -||-
    values = [146,189,115,400,92,83,91,98,63,60,78,62,44,54,110,66,109,91,69,226,59,89,67,82,95,62,75,86,56,78,643,201,39,87,81,76,94,92,88,84,241,43,55,27,73,75,84,89,71,175,99,87,104,138,59,67,52,74,124,66,58,97,68,77,38,68,346,74,62,89,37,94,52,99,187,125,86,141,54,147,451,47,52,63,85,61,58,92,97,58,63,87,111,51,86,49,42,88,63,93, 914,1022,1019,933,920,667,714,937,961,988,372,584,759,1023,951,902,541,971,951,562,897,987,578,689,898,872,589,638,617,1022,1023,798,761,987,869,341,936,856,719,926,364,489,364,658,798,918,937,962,872,1020,797,835,976,616,958,963,565,934,923,563,762,916,873,1023,533,889,651,1023,1023,719,583,651,746,364,1022,935,955,958,871,385,617,688,728,981,658,468,473,897,614,589,928,963,871,981,767,319,972,987,731,658, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    sleep_time = 1.05
    time.sleep(sleep_time)
    return random.choice(values)


# def readadc(SPICS, SPICLK, SPIMOSI, SPIMISO):
#     if ((potentiometer_adc > 7) or (potentiometer_adc < 0)):
#             return -1
    
#     GPIO.output(SPICS, True)
#     GPIO.output(SPICLK, False)  # start clock low
#     GPIO.output(SPICS, False)     # bring CS low

#     commandout = potentiometer_adc
#     commandout |= 0x18  # start bit + single-ended bit
#     commandout <<= 3    # we only need to send 5 bits here

#     for i in range(5):
#         if (commandout & 0x80):
#                 GPIO.output(SPIMOSI, True)
#         else:
#                 GPIO.output(SPIMOSI, False)
#         commandout <<= 1
#         GPIO.output(SPICLK, True)
#         GPIO.output(SPICLK, False)

#     adcout = 0
#     # read in one empty bit, one null bit and 10 ADC bits
#     for i in range(12):
#             GPIO.output(SPICLK, True)
#             GPIO.output(SPICLK, False)
#             adcout <<= 1
#             if (GPIO.input(SPIMISO)):
#                     adcout |= 0x1

#     GPIO.output(SPICS, True)
    
#     adcout >>= 1       # first bit is 'null' so drop it
#     return adcout