#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class DBStorage:
    """interaacts with the MySQL database"""

    classes = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    __engine = None
    __session = None

    def __init__(self):
        """ creates the engine self.__engine """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ returns a dictionary of all objects """
        obj_dict = {}
        if cls:
            obj_class = self.__session.query(self.classes.get(cls)).all()
            for item in obj_class:
                obj_dict[item.id] = item
            return obj_dict
        for class_name in self.CNC:
            if class_name == 'BaseModel':
                continue
            obj_class = self.__session.query(
                self.classes.get(class_name)).all()
            for item in obj_class:
                obj_dict[item.id] = item
        return obj_dict

    def new(self, obj):
        """ adds objects to current database session """
        self.__session.add(obj)

    def save(self):
        """ commits all changes of current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes obj from current database session if not None """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ creates all tables in database & session from engine """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """
            calls remove() on private session attribute (self.session)
        """
        self.__session.remove()

    def get(self, cls, id):
        """ retrieves one object """
        try:
            obj_dict = {}
            if cls:
                obj_class = self.__session.query(self.classes.get(cls)).all()
                for item in obj_class:
                    obj_dict[item.id] = item
            return obj_dict[id]
        except:
            return None

    def count(self, cls=None):
        """ counts number of objects in storage """
        obj_dict = {}
        if cls:
            obj_class = self.__session.query(self.classes.get(cls)).all()
            for item in obj_class:
                obj_dict[item.id] = item
            return len(obj_dict)
        else:
            for cls_name in self.classes:
                if cls_name == 'BaseModel':
                    continue
                obj_class = self.__session.query(self.CNC.get(cls_name)).all()
                for item in obj_class:
                    obj_dict[item.id] = item
            return len(obj_dict)
