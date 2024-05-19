#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.base_model import BaseModel


class DBStorage:
    """Private class attributes"""
    __engine = None
    __session = None

    def __init__(self):
        """
        link the engine with the MySQL database and user created before.
            * dialect: mysql
            * driver: mysqldb
        all values must be retrieved via environment variables:
            * MySQL user: HBNB_MYSQL_USER
            * MySQL password: HBNB_MYSQL_PWD
            * MySQL host: HBNB_MYSQL_HOST (here = localhost)
            * MySQL database: HBNB_MYSQL_DB
        don’t forget the option pool_pre_ping=True when you call create_engine
        drop all tables if the environment variable HBNB_ENV is equal to test
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                             pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        return: dictionary __objects:
            * key = <class-name>.<object-id>
            * value = object
        """
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                dic[key] = elem
        else:
            lista = [State, City, User, Place, Review, Amenity]
            for clase in lista:
                query = self.__session.query(clase)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    dic[key] = elem
        return (dic)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        - all classes who inherit from Base must be imported before calling.
        - create the current database session (self.__session) from the engine.
        - scoped_session - to make sure your Session is thread-safe
        """
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session

    def close(self):
        """ tarika bach ihayad """
        self.__session.remove()
