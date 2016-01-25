#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pingo

from events import Event

import logging
logger = logging.getLogger(__name__)


class Lock(object):
    """A lock object (serrure)"""

    def __init__(self, pin, lit_state=pingo.HIGH, time_opened=2):
        """Set lit_state to pingo.LOW to turn on led by bringing
           cathode to low state.

        :param lit_state: use pingo.HI for anode control, pingo.LOW
                          for cathode control
        """

        pin.mode = pingo.OUT
        self.pin = pin
        self.lit_state = lit_state
        self.blink_task = None
        self.time_opened = time_opened

    def open_and_close(self, session, reader_id, card):
        self._open()
        time.sleep(self.time_opened)
        self._close()
        logger.info("Open and close by %s" % card.id)

        event = Event(reader_id=reader_id,
                      typ='open_and_close', card_id=card.id)
        session.add(event)
        card.count += 1
        session.commit()

    def _open(self):
        if self.lit_state == pingo.HIGH:
            self.pin.high()
        else:
            self.pin.low()

    def _close(self):
        if self.lit_state == pingo.HIGH:
            self.pin.low()
        else:
            self.pin.high()

    @property
    def lit(self):
        return self.pin.state == self.lit_state

    @lit.setter
    def lit(self, new_state):
        if new_state:
            self.on()
        else:
            self.off()
