#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import pingo
from led import Led, BlinkTask
from lock import Lock
from button import PushButton
from factory import Factory


class Hardware(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._init_pins()
        self._init_parts()

    @abstractmethod
    def _init_pins(self):
        raise NotImplementedError()

    def _init_parts(self):
        self.r_led = Led(self.red_led_pin)
        self.g_led = Led(self.green_led_pin)
        self.lock = Lock(self.relay_pin)
        self.black_btn = PushButton(self.black_btn_pin)  # add button
        self.red_btn = PushButton(self.red_btn_pin)      # delete button

        self.r_led.off()
        self.g_led.off()
        # self.lock.open_and_close()


class RaspberryPiHardware(Hardware):
    def _init_pins(self):
        self.board = pingo.detect.get_board()

        self.red_led_pin = self.board.pins[12]    # GPIO18
        self.green_led_pin = self.board.pins[11]  # GPIO17

        self.relay_pin = self.board.pins[7]       # GPIO4

        self.black_btn_pin = self.board.pins[15]  # GPIO22
        self.red_btn_pin = self.board.pins[22]    # GPIO25


class GhostHardware(Hardware):
    def _init_pins(self):
        self.board = pingo.ghost.ghost.GhostBoard()

        self.red_led_pin = self.board.pins[0]
        self.green_led_pin = self.board.pins[1]

        self.relay_pin = self.board.pins[2]

        self.black_btn_pin = self.board.pins[12]
        self.red_btn_pin = self.board.pins[13]


_DEFAULT_HARDWARE_NAME = 'rpi'


class HardwareFactory(Factory):
    def __init__(self):
        super(HardwareFactory, self).__init__(Hardware, _DEFAULT_HARDWARE_NAME)
        self._register_all()

    def _register_all(self):
        self.register('rpi', RaspberryPiHardware)
        self.register('ghost', GhostHardware)


HARDWARE_FACTORY = HardwareFactory()
