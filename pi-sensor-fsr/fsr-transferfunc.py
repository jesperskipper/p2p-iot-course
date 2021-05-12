#!/usr/bin/env python

import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

## Global variables
DEBUG = 1

delay = 0.05 # 0.5, 0.25

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
potentiometer_adc = 0;


def readadc():
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

last_read = 0       # this keeps track of the last potentiometer value
tolerance = 40     # OLD: 40 to keep from being jittery we'll only change # OLD: 100

counter = 0

try:
    while True:
        pad_value = readadc()

        # V_out = (pad_value * 5) / 1023.0
        # V_out = V_out * 19.5
        # print("---------------------------------------")
        # print("V_out: %d" % V_out)

        pot_adjust = abs(pad_value - last_read)
        if ( pot_adjust > tolerance ):
            print("---------------------------------------")
            print("------------- BALLS IN ----------------")
            print("---------------------------------------")

            # print("Value pad_value: %d" % pad_value)
            # print("Value pad_adjust: %d" % pot_adjust)
            # print("Pressure Pad Value/10.24: %d" % (pad_value/10.24))
            last_read = pad_value
        else:
            print("-------------  NO NEW VAL   -----------")
        
        counter += 1
        if (counter == 100):
            print("--> 100 iter done")
            counter = 0
        time.sleep(delay)
except KeyboardInterrupt:
    GPIO.cleanup()
    pass




def testTolerance():
    i = 0
    last_reading = 0
    values = []
    while i < 1000:
        pad_value = readadc()
        abs_value = abs(pad_value - last_reading)
        print("%d: " % i)
        print("Value %d: " % abs_value)

        if (last_reading != 0):
            values.append(abs_value)
        
        last_reading = pad_value

        i += 1
        time.sleep(delay)
    
    print("------------------- DONE ------------")
    print("Max %d:" % max(values))
    print("Average %d:" % (sum(values) / len(values)) )

    GPIO.cleanup()


#print("Begining")
#testTolerance()
#print("The end")

