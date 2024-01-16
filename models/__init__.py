#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
