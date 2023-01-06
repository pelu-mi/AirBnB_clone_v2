#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_env
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    if storage_env == 'db':
        # For DBStorage
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), nullable=False, ForeignKey('states.id'))
    else:
        name = ''
        state_id = ''
