#!/usr/bin/python3
"""
Module - Base Model
"""


from datetime import datetime
import uuid
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

f_t = "%Y-%m-%dT%H:%M:%S.%f"  # ISO time format

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel():
    """
    Defines all common attributes/methods for other classes
    """
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initialize public class attributes:
        id - string - assign with an uuid when an instance is created.
        datetime objects:
        created_at -  assign  current datetime on instance creation
        updated_at - assign current datetime updated if object changes
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at


    def __str__(self):
        """
        override default private class method - __str__
        informal string representation of the BaseModel class
        returns - [<class name>] (<self.id>) <self.__dict__>
        """
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """
        public class method - save
        updates the public class attribute updated_at with current datatime
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        public class method - to_dict
        returns the dictionary representation of BaseModel class
        __class__ key set as holder for class name of the object
        display datetime format as:
        Year-Month-DayTHour:Minutes:Seconds.Milliseconds
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """
        public class method - delete
        deletes current instance from the file storage
        """
        models.storage.delete(self)
