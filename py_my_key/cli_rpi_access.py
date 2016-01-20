#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

#from rasp_access import rasp_access

import nxppy
import argparse

import time
import datetime

import RPi.GPIO as GPIO
import pingo
from pingo.parts.led import Led
from pingo.parts.button import Switch

import logging
import traceback
logging.Formatter.converter = time.gmtime
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

#DB_URI_DEFAULT = 'mysql+mysqlconnector://admin:admin@127.0.0.1:3306/admin'
DB_URI_DEFAULT = 'sqlite:///cards.db'

Base = declarative_base()


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

    #def open_and_close(self, session, reader_id, card_id):
    def open_and_close(self, session, reader_id, card):
        self._open()
        time.sleep(self.time_opened)
        self._close()
        #logger.info("Open and close by %s" % card_id)
        logger.info("Open and close by %s" % card.id)

        #event = Event(reader_id=reader_id, card_id=card_id)
        event = Event(reader_id=reader_id, typ='open_and_close', card_id=card.id)
        session.add(event)
        card.count += 1
        session.commit()
          
    def _open(self):
        #logger.debug("Open")
        if self.lit_state == pingo.HIGH:
            self.pin.high()
        else:
            self.pin.low()

    def _close(self):
        #logger.debug("Close")
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


"""
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
   firstname = Column(String(60), nullable=False)

    card_id = Column(String(60), ForeignKey("cards.id"), nullable=True, unique=True)

    #last_event_id = Column(Integer, ForeignKey("events.card_id"))
    events_count = Column(Integer, default=0)

    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())
"""

class Card(Base):
    __tablename__ = 'cards'

    id = Column(String(60), primary_key=True)
    is_master = Column(Boolean, default=False)
    count = Column(Integer, default=0)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())    
    
class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)   
    reader_id = Column(Integer, ForeignKey("readers.id"))
    typ = Column(String(60), nullable=False)

    card_id = Column(Integer, ForeignKey("cards.id"))
    other_card_id = Column(Integer, ForeignKey("cards.id"), default="")

    created = Column(DateTime, default=func.now())
    
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
                

class App(object):
    def __init__(self, db_uri):
        self.db_uri = db_uri

        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        self.board = pingo.detect.get_board()

        red_led_pin = self.board.pins[12]   #GPIO18
        self.r_led = Led(red_led_pin)
        green_led_pin = self.board.pins[11] #GPIO17
        self.g_led = Led(green_led_pin)
        
        pin_relay = self.board.pins[7] #GPIO4
        self.lock = Lock(pin_relay)
        
        self.r_led.off()
        self.g_led.off()
        #self.lock.open_and_close()
        
        black_btn_pin = self.board.pins[15] #GPIO22
        self.black_btn = Switch(black_btn_pin)
        red_btn_pin = self.board.pins[22]   #GPIO25
        self.red_btn = Switch(red_btn_pin)

    def create_readers(self):
        reader = Reader(comment='First reader')
        self.session.add(reader)
        self.session.commit()

    def reader(self, id=None):
        if id is None:
            return self.session.query(Reader).one()  # get the first reader
        else:
            return self.session.query(Reader).filter(Reader.id == id).one()

    def run(self, reader):      
        
        count_total = self.session.query(Card).count()
        if count_total == 0: 
            logger.info("No card in DB - waiting for a first card which will be considered as Master")

        for card_id in reader.reading():
            count_total = self.session.query(Card).count()
            if count_total == 0:
                #No card in db, so we add automatically the card in the db as master
                card = Card(id=card_id, is_master=True)
                self.session.add(card)

                event = Event(reader_id=reader.id, typ='add_master', card_id=card_id)
                self.session.add(event)
                
                self.session.commit()
                logger.info("Card %s have been added to DB and is considered as Master" % card_id)
                
            else:
                #There is at least one card in db
                #We test if the card detected exist in db
                count = self.session.query(Card).filter(Card.id == card_id).count()
                if count == 0:
                    #Detected card is not in the db
                    event = Event(reader_id=reader.id, typ='open_not_allowed', card_id=card_id)
                    self.session.add(event)
                    self.session.commit()
                    
                    logger.info("card %s doesn't exist" % card_id)
                else: # count==1
                    #The detected card is in the db
                    #We get the card entry of the db with the card_id
                    card = self.session.query(Card).filter(Card.id == card_id).one()
                    if card.is_master:
                        #The detected card is a master card
                        
                        if self.black_btn.pin.state == pingo.LOW and self.red_btn.pin.state == pingo.HIGH:
                            #Only BLACK button was pressed
                            logger.info("Waiting to add a card by master %s" % card_id)
                            card_id_to_add = reader.read(card_id)
                            count_card_to_add = self.session.query(Card).filter(Card.id == card_id_to_add).count()
                            if count_card_to_add == 0 and card_id_to_add is not None:
                                logger.info(card_id_to_add)
                                card = Card(id=card_id_to_add, is_master=False)
                                self.session.add(card)
                                
                                event = Event(reader_id=reader.id, typ='add', card_id=card_id, other_card_id=card_id_to_add)
                                self.session.add(event)
                                
                                self.session.commit()
                                logger.info("Card %s have been added to DB" % card_id_to_add)
                            elif card_id_to_add is None:
                                logger.info("Time up to add a new card")
                            else:
                                logger.info("Card %s ever exists into DB" % card_id_to_add)

                        elif self.black_btn.pin.state == pingo.HIGH and self.red_btn.pin.state == pingo.LOW:
                            #Only RED button was pressed
                            logger.info("Waiting to remove a card by master %s" % card_id)
                            card_id_to_remove = reader.read(card_id)
                            count_to_remove = self.session.query(Card).filter(Card.id == card_id_to_remove).count()
                            if count_to_remove > 0:
                                self.session.query(Card).filter(Card.id == card_id_to_remove).delete()
                                event = Event(reader_id=reader.id, typ='remove', card_id=card_id, other_card_id=card_id_to_remove)
                                self.session.add(event)
                                self.session.commit()
                                logger.info("Card %s have been removed from DB" % card_id_to_remove)
                            else:
                                logger.info("Card %s can't be removed because it doesn't exists into DB" % card_id_to_remove)
                        
                        elif self.black_btn.pin.state == pingo.LOW and self.red_btn.pin.state == pingo.LOW:
                            #The TWO buttons were pressed
                            
                            logger.info("Waiting to remove or add a Master card by master %s" % card_id)
                            card_id_to_treat = reader.read(card_id)
                            if card_id_to_treat is not None:
                                count_card_to_treat = self.session.query(Card).filter(Card.id == card_id_to_treat).count()
                                if count_card_to_treat == 0:
                                    card = Card(id=card_id_to_treat, is_master=True)
                                    self.session.add(card)
                                    event = Event(reader_id=reader.id, typ='add_master', card_id=card_id, other_card_id=card_id_to_treat)
                                    self.session.add(event)
                                    self.session.commit()
                                    logger.info("Card %s have been added as Master to DB" % card_id_to_treat)
                                else:
                                    count_masters = self.session.query(Card).filter(Card.is_master == True).count()
                                    if count_masters > 1:
                                        self.session.query(Card).filter(Card.id == card_id_to_treat).delete()
                                        event = Event(reader_id=reader.id, typ='remove_master', card_id=card_id, other_card_id=card_id_to_treat)
                                        self.session.add(event)
                                        self.session.commit()
                                        logger.info("Card %s have been removed from DB" % card_id_to_treat)
                                    #else:
                                        #logger.info("This master card can't be delete because it the last one")
                            else:
                                logger.info("No master card has been deleted")    
                            
                            
                        else:
                            #NO button was pressed (master card)
                            #Master card just want to open the door
                            #self.lock.open_and_close(self.session, reader.id, card_id)
                            self.lock.open_and_close(self.session, reader.id, card)
                    else:
                        #An authorized card was detected
                        #self.lock.open_and_close(self.session, reader.id, card_id)
                        self.lock.open_and_close(self.session, reader.id, card)
                
            #logger.debug("Card_id: %r" % card_id)

    def stats(self, tz_from='', tz_to=''):
        import pandas as pd
        from tzlocal import get_localzone
        df_events = pd.read_sql("events", self.db_uri)
        #df_cards = pd.read_sql("cards", self.db_uri, index_col='id')
        df_students = pd.read_sql("students", self.db_uri, index_col='id')[['name', 'firstname', 'card_id']]
        df_merged = pd.merge(df_events, df_students)
        if tz_from == '':
            tz_from = 'UTC'
        if tz_to == '':
            tz_to = get_localzone() # 'Europe/Paris'
        df_merged['created'] = df_merged['created'].dt.tz_localize(tz_from).dt.tz_convert(tz_to)
        df_merged = df_merged.sort_values(['reader_id', 'id'], ascending=[True, False]).set_index(['reader_id', 'id'])
        df_merged = df_merged[['created', 'card_id', 'name', 'firstname']]
        print(df_merged)
        df_merged['created'] = df_merged['created'].dt.tz_localize(None)
        df_merged.to_excel('cards.xlsx')

def main():
    parser = argparse.ArgumentParser(prog="main", description='Card')
    parser.add_argument('--reader', help="Reader id", default=1)
    parser.add_argument('--db_uri', help="Database URI", default=DB_URI_DEFAULT)
    parser.add_argument('--init', dest='init', action='store_true')
    parser.add_argument('--stats', dest='stats', action='store_true')
    args = parser.parse_args()

    db_uri = args.db_uri
    if args.stats:
        my_app = App(db_uri)
        my_app.stats()
    elif args.init:
        my_app = App(db_uri)
        logger.info("Create readers")
        my_app.create_readers()

        #logger.info("Créer etu")
        #my_app.creer_students()
    else:
        while(True):
            try:
                my_app = App(db_uri)
                reader = my_app.reader(args.reader)
                logger.info("Waiting for a card on reader %d - %s" % (reader.id, reader.comment))
                my_app.run(reader)
            except (KeyboardInterrupt, SystemExit):
                logger.info("Quit by CTRL+C")
                break
            except Exception as e:
                logger.error(traceback.format_exc())
                logger.error("Try again")
                time.sleep(2)


if __name__ == '__main__':
    main()
