#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pingo
from led import Led
import time


board = pingo.detect.get_board()
red_led_pin = board.pins[12]    # GPIO18
r_led = Led(red_led_pin)

r_led.blink(times=10, on_delay=0.1, off_delay=None)
print(r_led.blinkThread.isAlive())

while(r_led.blinkThread.active):
    # if(r_led.blinkThread.isAlive()):
    print(r_led.blinkThread.active)
    time.sleep(0.5)
print(r_led.blinkThread.isAlive())
