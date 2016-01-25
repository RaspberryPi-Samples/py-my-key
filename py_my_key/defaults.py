#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base

# DB_URI_DEFAULT = 'mysql+mysqlconnector://admin:admin@127.0.0.1:3306/admin'
DB_URI_DEFAULT = 'sqlite:///cards.db'

Base = declarative_base()
