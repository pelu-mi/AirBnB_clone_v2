#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_env
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    if storage_env == 'db':
        # For DBStorage
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                          cascade='all, delete, delete-orphan')
    else:
        # For FileStorage
        name = ''

        @property
        def cities(self):
            """ Return list of City instances where
                state_id = current State.id
            """
            from models import storage
            related_cities = []
            all_cities = storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    related_cities.append(city)
            return related_cities
