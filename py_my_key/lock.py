#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pingo

from events import Event

import logging
logger = logging.getLogger(__name__)


class Lock(object):
    """A lock object (serrure)"""

    def __init__(self, pin, opened_state=pingo.HIGH, time_opened=5):
        """Set opened_state to pingo.LOW to turn on led by bringing
           cathode to low state.

        :param opened_state: use pingo.HI for anode control, pingo.LOW
                          for cathode control
        """

        pin.mode = pingo.OUT
        self.pin = pin
        self.opened_state = opened_state
        self.time_opened = time_opened

    def open_and_close(self, session, reader_id, card):
        logger.info("Open and close by %s" % card.id)
        self._open()
        time.sleep(self.time_opened)
        self._close()

        event = Event(reader_id=reader_id,
                      typ='open_and_close', card_id=card.id)
        session.add(event)
        card.count += 1
        session.commit()

    def _open(self):
        if self.opened_state == pingo.HIGH:
            self.pin.high()
        else:
            self.pin.low()

    def _close(self):
        if self.opened_state == pingo.HIGH:
            self.pin.low()
        else:
            self.pin.high()

    @property
    def opened(self):
        return self.pin.state == self.opened_state

    @opened.setter
    def opened(self, new_state):
        if new_state:
            self._open()
        else:
            self._close()
