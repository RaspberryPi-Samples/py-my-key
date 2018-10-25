#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_py_my_key
----------------------------------

Tests for `py_my_key` module.
"""

import os
from nose.tools import assert_equal

from py_my_key.cli_rpi_access import App
from py_my_key.events import Event


class TestPyMyKey:

    def setUp(self):
        filename = 'cards_test.db'
        self.db_uri = 'sqlite:///' + filename
        try:
            os.remove(filename)
        except OSError:
            pass
        self.hardware_name = 'ghost'
        self.reader_name = 'test'
        self.reader_id = 1
        #  print("setup")

    def tearDown(self):
        pass
        # print("tearDown")

    def test_000_something(self):
        my_app = App(self.db_uri, self.hardware_name, self.reader_name)
        my_app.hw.lock.time_opened = 0
        my_app.create_reader()  # init
        reader = my_app.reader(self.reader_id)
        reader.initialize()
        reader.initialize_data(['A0000000',
                                'A0000001',
                                'A0000000', 'A0000001',
                                'A0000000',
                                'A0000001'])
        my_app._at_startup()

        # First card (A0000000) is set as master
        card_id = reader._read()
        my_app._process(reader, card_id)
        # time.sleep(1)

        # A0000001 try to enter but is not allowed
        card_id = reader._read()
        my_app._process(reader, card_id)
        # my_app._hw.black_btn.press()

        # Allow A0000001 to enter (by A0000000)
        my_app.hw.black_btn.press()
        card_id = reader._read()
        my_app._process(reader, card_id)
        my_app.hw.black_btn.release()

        # A0000000 enter
        card_id = reader._read()
        my_app._process(reader, card_id)

        # A0000001 enter
        card_id = reader._read()
        my_app._process(reader, card_id)

        assert_equal(my_app.session.query(Event).count(), 5)
