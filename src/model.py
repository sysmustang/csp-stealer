from src import db, webapp
from sqlalchemy import Column, Integer, String, DateTime, TEXT
import datetime
import os


class Event(db.Model):
    __tablename__ = 'event'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    ip = Column('ip', String, nullable=False)
    url = Column('url', TEXT)
    dom = Column('dom', TEXT)
    cookie = Column('cookie', TEXT)
    localstorage = Column('localstorage', TEXT)
    csp_policy = Column('csp_policy', String)
    referrer = Column('referrer', TEXT)
    useragent = Column('useragent', String)
    img_path = Column('img_path', String)
    date = Column('date', DateTime, default=datetime.datetime.utcnow())


if not os.path.exists('../xss.db'):
    with webapp.app_context():
        db.create_all()
        db.session.commit()
