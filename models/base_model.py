#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Table, ForeignKey

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(
        String(60), unique=True, nullable=False, primary_key=True
    )
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow()
    )
    created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow()
    )

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    try:
                        value = datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f"
                        )
                    except ValueError:
                        value = datetime.now()
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Convert the base model object to dict

        Returns: a dictionary consisting of
        attribute names of the base model object as keys of the dictionary
        and their values as values of the dictionary
        """
        dct = dict(self.__dict__)
        dct["__class__"] = self.__class__.__name__
        dct["created_at"] = self.created_at.isoformat()
        dct["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in dct.keys():
            del dct["_sa_instance_state"]
        return dct

    def delete(self):
        """delete the current instance from the storage"""
        storage.delete(self)
