#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv
import models


class Amenity(BaseModel, Base):
    """amenity"""

    if models.storage_type:
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
    else:
        name = ""
