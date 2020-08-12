#!/usr/bin/python3
"""
Module - File Storage
"""


import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file
    to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Public instance method
        Returns the dictionary __objects
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__:
                    new_dict[key] = value
            return new_dict
        return (self.__objects)

    def new(self, obj):
        """
        Public instance method
        Sets in __objects the obj with key <obj class name>.id
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Public instance method
        Serializes __objects to the JSON file (path: __file_path)
        """
        item = {}
        for key in self.__objects:
            item[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as my_file:
            json.dump(item, my_file)

    def reload(self):
        """
        Public instance method
        deserializes the JSON file to __objects
        """
        try:
            with open(self.__file_path, 'r') as my_file:
                item = json.load(my_file)
            for k in item:
                self.__objects[k] = classes[item[k]["__class__"]](**item[k])
        except:
            pass

    def delete(self, obj=None):
        """
        Public instance method
        delete obj from __objects if its inside
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
