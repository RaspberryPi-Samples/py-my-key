#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pingo


class PushButton(object):
    """A single Push button"""
    def __init__(self, pin, pressed_state=pingo.LOW):
        """Set pressed_state to pingo.LOW when button is pressed
        :param pin: A instance of DigitalPin
        :param pressed_state: use pingo.LOW for pull-up,
            pingo.HIGH for pull-down
        """
        pin.mode = pingo.IN
        self.pin = pin
        self._pressed_state = pressed_state
        d = {
            pingo.LOW: pingo.HIGH,
            pingo.HIGH: pingo.LOW,
        }
        self._released_state = d[pressed_state]
        if isinstance(self.pin.board, pingo.ghost.ghost.GhostBoard):
            self.pin.board._set_pin_state(self.pin, self._released_state)

    def _test_pin_instance(self):
        if not isinstance(self.pin.board, pingo.ghost.ghost.GhostBoard):
            raise(NotImplementedError('pin from a GhostBoard is required'))
        elif not isinstance(self.pin, pingo.board.DigitalPin):
            raise(NotImplementedError('DigitalPin is required'))

    def press(self):
        self._test_pin_instance()
        board = self.pin.board
        pin = self.pin
        board._set_pin_state(pin, self._pressed_state)

    def release(self):
        self._test_pin_instance()
        board = self.pin.board
        pin = self.pin
        board._set_pin_state(pin, self._released_state)

    @property
    def pressed(self):
        return True if self.pin.state == self._pressed_state else False

    @property
    def released(self):
        return True if self.pin.state == self._released_state else False
