"""
@file 

@details Full-Stack-Foundations Lesson 1
@ref https://github.com/udacity/Full-Stack-Foundations/blob/master/Lesson_1/database_setup.py
"""

import os

# Configuration 
# Configuration is 1 of 4 parts of SQLAlchemy database creation
# Configuration at beginning of file
# - imports all modules needed
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# - creates instance of declarative base.
Base = declarative_base()

# Class, 2 of 4 parts of SQLAlchemy database creation
# representation of table as a python class
# extends Base class
# nested inside will be table and mapper code.
class Restaurant(Base):

    # Table, 3 of 4 parts of SQLAlchemy database creation
    # representation of table inside database
    __tablename__ = 'restaurant'

    # Mapper, 4 of 4 parts of SQLAlchemy database creation
    # maps python objects to columns in database

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


# Class, 2 of 4 parts of SQLAlchemy database creation
# representation of table as a python class
# extends Base class
class MenuItem(Base):

    # Table, 3 of 4 parts of SQLAlchemy database creation
    # representation of table inside database
    __tablename__ = 'menu_item'

    # Mapper, 4 of 4 parts of SQLAlchemy database creation
    # maps python objects to columns in database

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    # 'restaurant.id' says, go to table of the relationship, Restaurant, look
    # up .id member, and set restaurant_id to this .id value.
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


# Configuration - at end of file
# - creates (or connects) database and adds tables and columns
engine = create_engine('sqlite:///restaurantmenu.db')


Base.metadata.create_all(engine)