"""The application's model objects"""

#from sqlalchemy.orm import mapper

import sqlalchemy as sa

from sqlalchemy import orm, and_
from sqlalchemy.orm import relation, backref, eagerload, eagerload_all

from sqlalchemy import Integer, String, DateTime
from sqlalchemy import Table, Column, MetaData, ForeignKey

from sqlalchemy.orm.exc import NoResultFound 

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from annikki.model import meta
from annikki.model.meta import Session as s

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


class Deck(Base):
    __tablename__ = "deck"

    id = Column(Integer, primary_key = True)
    user_deck_id = Column(Integer)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.uid'))
    user = relation((lambda: annikki.model.User), backref=backref('deck', order_by=name))

    def __init__(self, user_id, user_deck_id, name):
        self.user_id = user_id
        self.user_deck_id = user_deck_id
        self.name = name

    @classmethod
    def find_or_create(klz, user_id, name):
        try:
            deck = s.query(Deck).filter(and_(Deck.name == name, Deck.user_id == user_id)).one()
        except NoResultFound, e:
            deck = Deck(user_id, user_deck_id, name)
            s.add(deck)
            s.commit()
        return deck

class Card(Base):
    __tablename__ = "card"

    id = Column(Integer, primary_key = True)
    user_card_id = Column(Integer) #id in the user's db
    question = Column(String)
    answer = Column(String)
    user_id = Column(Integer, ForeignKey('users.uid'))
    user = relation((lambda: annikki.model.User), backref=backref('card'))
    deck_id = Column(Integer, ForeignKey('deck.id'))
    deck = relation(Deck, backref=backref('card'))

    def __init__(self, user_id, deck_id, user_card_id, question, answer):
        self.user_id = user_id
        self.user_card_id = user_card_id
        self.question = question
        self.deck_id = deck_id
        self.answer = answer

    @classmethod
    def find_or_create(klz, user_id, deck_id, user_card_id, question, answer):
        try:
            card = s.query(Card).filter(and_(Card.user_card_id == user_card_id, Card.user_id == user_id)).one()
        except NoResultFound, e:
            card = Card(user_id, deck_id, user_card_id, question, answer)
            s.add(card)
            s.commit()
        return card



class ReviewSet(Base):
    __tablename__ = "review_set"

    id = Column(Integer, primary_key = True)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.uid'))
    user = relation((lambda: annikki.model.User), backref=backref('review_sets'))
    #deck_id = Column(Integer, ForeignKey('deck.id'))
    #deck = relation(Deck, backref=backref('review_sets'))
    
    def __init__(self, timestamp, user_id):
        self.timestamp = timestamp
        self.user_id = user_id
        #self.deck_id = deck_id

    @classmethod
    def all():
        s.query(ReviewSet).option(eagerload_all('reviews.card'), eagerload('user'))

class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key = True)
    timestamp = Column(DateTime)
    ease = Column(Integer)
    card_id = Column(Integer, ForeignKey('card.id'))
    card = relation(Card, backref=backref('review', order_by=timestamp))
    review_set_id = Column(Integer, ForeignKey('review_set.id'))
    review_set = relation(ReviewSet, backref = backref('reviews'))

    def __init__(self, card_id, timestamp, ease):
        self.card_id = card_id
        self.timestamp = timestamp
        self.ease = ease


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
