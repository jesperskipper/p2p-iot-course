#!/usr/bin/env python

import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

## Global variables
DEBUG = 1
delay = 0.5

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
tolerance = 100     # to keep from being jittery we'll only change

try:
    while True:
        pad_value = readadc()

        pot_adjust = abs(pad_value - last_read)

        if ( pot_adjust > tolerance ):
            print("---------------------------------------")
            print("Value: %d" % pad_value)
            # print("Pressure Pad Value/10.24: %d" % (pad_value/10.24))
            last_read = pad_value
        else:
            print("-------------  NO NEW VAL   -----------")
        
        time.sleep(delay)
except KeyboardInterrupt:
    GPIO.cleanup()
    pass