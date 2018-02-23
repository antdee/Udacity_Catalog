#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
        }

class Room(Base):
    __tablename__ = "room"

    name = Column(String(250), primary_key=True)
    #description = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
        }

class Product(Base):
    """docstring for Item"""
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    price = Column(String(8))
    image = Column(String(250))
    room = Column(String, ForeignKey('room.name'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user_picture = Column(String(250))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image': self.image,
            'room': self.room,
            'user_id': self.user_id,
            'user_picture': self.user_picture,
        }

engine = create_engine('sqlite:///furniture.db')

Base.metadata.create_all(engine)

