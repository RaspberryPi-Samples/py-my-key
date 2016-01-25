#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

from defaults import Base

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)   
    reader_id = Column(Integer, ForeignKey("readers.id"))
    typ = Column(String(60), nullable=False)

    card_id = Column(Integer, ForeignKey("cards.id"))
    other_card_id = Column(Integer, ForeignKey("cards.id"), default="")

    created = Column(DateTime, default=func.now())
   