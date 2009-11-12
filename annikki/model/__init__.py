"""The application's model objects"""

#from sqlalchemy.orm import mapper

import sqlalchemy as sa

from sqlalchemy import orm
from sqlalchemy.orm import relation, backref

from sqlalchemy import Integer, String, DateTime
from sqlalchemy import Table, Column, MetaData, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from annikki.model import meta

from authkit.users.sqlalchemy_driver.sqlalchemy_05 import UsersFromDatabase

import annikki

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine

    meta.metadata = Base.metadata

class StudyLog(Base):
    __tablename__ = "studylog"
    
    id = Column(Integer, primary_key = True)
    deck = Column(String)
    count = Column(Integer)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.uid'))
    user = relation((lambda: annikki.model.User), backref=backref('studylogs', order_by=timestamp))
     
    def __init__(self, user, deck, count, timestamp):
        self.user = user
        self.deck = deck
        self.count = count
        self.timestamp = timestamp
        
    def __repr__(self):
        return "<StudyLog(user='%s','%s','%s', '%s')>" % (self.user.name, self.deck, self.count, self.timestamp)

"""

## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass
"""
