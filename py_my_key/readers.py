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
from factory import Factory

class BaseReader(Base):
    __tablename__ = 'readers'
    
    id = Column(Integer, primary_key=True)
    comment = Column(String(60))
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def _read(self):
        logger.info("BaseReader _read")
    
    def reading(self):
        data_prev = ''
        td_limit = datetime.timedelta(seconds=5)
        dt_prev = datetime.datetime.utcnow()
        while(True):
            data = self._read()
            if data is not None:
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
            if card_id is not None and card_id != card_id_master:
                break
            if dt - dt_start_waiting_card > td_limit:
                card_id = None
                break
        return card_id


class NxppyReader(BaseReader):
    def _read(self):
        mifare = nxppy.Mifare()
        data = ''
        try:
            data = mifare.select()
        except nxppy.SelectError:
            pass
        if data != '':
            return data
        else:
            return None

class TestReader(BaseReader):
    def initialize_data(self, lst_data):
        self._lst_data = lst_data
        self._i = -1

    def _read(self):
        self._i += 1
        return self._lst_data[self._i]

    def reading(self):
        for data in self._lst_data:
            yield data

_DEFAULT_READER_NAME = 'nxppy'
        
class ReaderFactory(Factory):
    def __init__(self):
        super(ReaderFactory, self).__init__(BaseReader, _DEFAULT_READER_NAME)
        self._register_all()
    
    def _register_all(self):
        self.register('nxppy', NxppyReader)
        self.register('test', TestReader)


READER_FACTORY = ReaderFactory()
