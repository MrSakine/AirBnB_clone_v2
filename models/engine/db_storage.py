#!/usr/bin/python3
"""DATABASE engine"""

from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine


class DBStorage:
    """Database engine"""

    __engine = None
    __session = None

    def __init__(self):
        """init"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True,
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """get all objects"""
        my_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for q in query:
                key = "{}.{}".format(type(q).__name__, q.id)
                my_dict[key] = q
        else:
            class_list = [State, City, Place, Amenity, Review, User]
            for c in class_list:
                query = self.__session.query(c)
                for q in query:
                    key = "{}.{}".format(type(q).__name__, q.id)
                    my_dict[key] = q
        return my_dict

    def new(self, obj):
        """add new element"""
        self.__session.add(obj)

    def save(self):
        """save changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete element"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reload"""
        Base.metadata.create_all(self.__engine)
        make_session = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(make_session)
        self.__session = Session()

    def close(self):
        """close Session"""
        self.__session.close()
