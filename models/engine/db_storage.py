#!/usr/bin/Python3
""" This module defines the engine for the MySQL database """

from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


classes = {"City": City, "State": State, "User": User, "Place": Place,
           "Review": Review, "Amenity": Amenity}


class DBStorage:
    """ Defining the class DBStorage """
    __engine = None
    __session = None

    user = os.getenv('HBNB_MYSQL_USER')
    pwd = os.getenv('HBNB_MYSQL_PWD')
    host = os.getenv('HBNB_MYSQL_HOST')
    db = os.getenv('HBNB_MYSQL_DB')
    env = os.getenv('HBNB_ENV')

    def __init__(self):
        """ Contructor for the class DBStorage """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)
    if env == "test":
        Base.MetaData.drop_all(self.__engine)

    def all(self, cls=None):
        """ Method to return a dictionary of objects """
        new_dict = {}
        if cls:
            if type(cls) == str:
                cls = classes[cls]

            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + "." + obj.id
                new_dict[key] = obj
        else:
            for clas in classes.values():
                objs = self.__session.query(clas).all()

                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """ Method to add a new object to the current database """
        self.__session.add(obj)

    def save(self):
        """ Method to commit all changes to the current database """
        self.__session.commit()

    def delete(self, obj=None):
        """ Method to delete a new object to the current database """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Method to create the current database session """
        Base.metadata.create_all(self.__engine)
        sesn_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sesn_factory)
        self.__session = Session()

    def close(self):
        """ Method to close database session """
        self.__session.close()
