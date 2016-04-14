#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pingo
from pingo.parts.led import Led
from time import sleep

board = pingo.detect.get_board()
led_pin = board.pins[11]
led = Led(led_pin)

led.blink(times=0, on_delay=0.8, off_delay=0.2) # blink foreever

while(True):
    led.blink(times=5, on_delay=0.8, off_delay=0.2) # blink foreever
    sleep(10)
