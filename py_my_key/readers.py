#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func


import logging
import traceback
logger = logging.getLogger(__name__)

try:
    import nxppy
    _HAS_NXPPY = True
except ImportError:
    _HAS_NXPPY = False
    logger.warning("Can't import nxppy")

from defaults import Base

class Reader(Base):
    __tablename__ = 'readers'
    
    id = Column(Integer, primary_key=True)
    comment = Column(String(60))
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())

    
    def _read(self):
        mifare = nxppy.Mifare()
        data = ""
        try:
            data = mifare.select()
        except nxppy.SelectError:
            pass
        return data    
    
    def reading(self):
        data_prev = ''
        td_limit = datetime.timedelta(seconds=5)
        dt_prev = datetime.datetime.utcnow()
        while(True):
            data = self._read()
            if data != '' and data is not None:
                #logger.debug("UID=" + str(data))
                dt = datetime.datetime.utcnow()
                
                if data != data_prev:
                    yield data
                else:
                    if dt - dt_prev > td_limit:
                        yield data
                
                data_prev = data
                dt_prev = dt

    def read(self, card_id_master, td_limit=datetime.timedelta(seconds=10)):
        dt_start_waiting_card = datetime.datetime.utcnow()
        while True:
            dt = datetime.datetime.utcnow()
            card_id = self._read()
            if card_id != '' and card_id is not None and card_id != card_id_master:
                break
            if dt - dt_start_waiting_card > td_limit:
                card_id = None
                break
        return card_id
