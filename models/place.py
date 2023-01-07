#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, Integer, Float, ForeignKey


if storage_type == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),nullable=False,
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),nullable=False,
                                 primary_key=True))

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if storage_type == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place',
                               cascade='all, delete, delete-orphan')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """ Return list of Review objects where
                review.place_id = current Place.id
            """
            from models import storage
            all_revs = storage.all(Review)
            objs = []
            for r in all_revs.values():
                if r.place_id == self.id:
                    objs.append(r)
            return objs

        @property
        def amenities(self):
            """ Return list of Amenities available in a place
            """
            from models import storage
            all_amens = storage.all(Amenity)
            objs = []
            for a in all_amens.values():
                if a.id in self.amenity_ids:
                    objs.append(a)
            return objs

        @amenities.setter
        def amenities(self, obj):
            """ Amenities setter
            """
            if obj is not None:
                if isinstance(obj, Amenity):
                    if obj.id not in self.amenity_ids:
                        self.amenity_ids.append(obj.id)
