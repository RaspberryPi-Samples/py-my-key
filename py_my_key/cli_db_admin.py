#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from defaults import DB_URI_DEFAULT, Base

from events import Event
from readers import BaseReader
from cards import Card


class ReaderView(ModelView):
    column_display_pk = True
    can_create = False
    can_edit = False
    can_delete = False
    page_size = 50


class CardView(ModelView):
    column_display_pk = True
    can_create = False
    can_edit = False
    can_delete = False
    page_size = 50


class EventView(ModelView):
    column_display_pk = True
    can_create = False
    can_edit = False
    can_delete = False
    page_size = 50


def main():
    parser = argparse.ArgumentParser(prog="main", description='Card')
    parser.add_argument('--db_uri', help="Database URI",
                        default=DB_URI_DEFAULT)
    args = parser.parse_args()

    app = Flask(__name__)

    admin = Admin(app, name='py-my-key', template_mode='bootstrap3')
    # Add administrative views here

    # Flask and Flask-SQLAlchemy initialization here

    engine = create_engine(args.db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    admin.add_view(ReaderView(BaseReader, session, "Reader"))
    admin.add_view(CardView(Card, session))
    admin.add_view(EventView(Event, session))

    app.run()

if __name__ == '__main__':
    main()
