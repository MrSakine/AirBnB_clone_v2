#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
import shlex
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from os import getenv
import models

if models.storage_type == "db":
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True,
        ),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            primary_key=True,
        ),
    )


class Place(BaseModel, Base):
    """A place to stay"""

    if models.storage_type == "db":
        __tablename__ = "places"
        amenity_ids = []
        city_id = Column(
            String(60), ForeignKey("cities.id"), nullable=False
        )
        user_id = Column(
            String(60), ForeignKey("users.id"), nullable=False
        )
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            "Review", backref="place", cascade="all, delete"
        )
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            backref="place_amenities",
        )
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

    if models.storage_type == "db":

        @property
        def reviews(self):
            """The reviews property"""
            all_storage = models.storage.all()
            elements = []
            result = []
            for key in all_storage:
                city = key.replace(".", " ")
                city = shlex.split(city)
                if city[0] == "Review":
                    elements.append(all_storage[key])
            for e in elements:
                if e.place_id == self.id:
                    result.append(e)
            return result

        @property
        def amenities(self):
            """Get amenities"""
            return []

        @amenities.setter
        def amenities(self, obj):
            """Add a new amenity to @amenity_ids"""
            if obj.__class__.__name__ == "Amenity":
                name = obj.__class__.__name__
                amenity_ids.append("{0}.{1}".format(name, obj.id))
