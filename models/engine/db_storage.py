#!/usr/bin/python3
""" DB Storage Module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv


classes = {
            'User': User, 'Place': Place, 'State': State,
            'City': City, 'Amenity': Amenity, 'Review': Review
          }

class DBStorage:
    """ Class defining DB Storage using SQLalchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the new dbstorage"""
        USR = getenv('HBNB_MYSQL_USER')
        PWD = getenv('HBNB_MYSQL_PWD')
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')
        ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                        USR, PWD, HOST, DB), pool_pre_ping=True)
        if ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Return all objects in storage
        """
        objs = {}
        if cls is None:
            for c in classes:
                query = self.__session.query(c).all()
                for obj in query:
                    key = obj.__class__.__name__ + '.' + obj.id
                    objs[key] = obj
        else:
            query = self.__session.query(cls).all()
            for obj in query:
                key = obj.__class__.__name__ + '.' + obj.id
                objs[key] = obj
        return objs

    def new(self, obj):
        """ Add object to current database session
        """
        if obj is None:
            return
        try:
            self.__session.add(obj)
            self.__session.flush()
            self.__session.refresh(obj)
        except Exception as e:
            self.__session.rollback()
            raise e

    def save(self):
        """ Commit changes to session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete an object from current db session
        """
        if obj is None:
            return
        cls = type(obj)
        self.__session.query(cls).filter(cls.id == obj.id).delete()

    def reload(self):
        """ Create all tables in DB and create the DB session
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)()

    """def close():
        "" Close the session""
        self.__session.close()
        """
