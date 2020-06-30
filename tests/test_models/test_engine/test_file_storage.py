#!/usr/bin/python3
"""Unittest for File Storage
"""
import unittest
import models
from models import storage
from models.base_model import BaseModel
from models.engine import file_storage
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import models.base_model
import json
import pep8
import sys
import io
from datetime import datetime
import inspect
import uuid
import time
import os


classes = {"BaseModel": BaseModel, "User": User, "State": State,
           "City": City, "Amenity": Amenity, "Place": Place,
           "Review": Review}


class TestDocsFileStorage(unittest.TestCase):
    """SI FUNCIONAN LAS DE DOCUMENTACION
    check for documentation """

    def test_module_doc(self):
        """ check for module documentation """
        self.assertTrue(len(models.engine.file_storage.__doc__) > 0)

    def test_class_doc(self):
        """ check for documentation """
        self.assertTrue(len(FileStorage.__doc__) > 0)

    def test_method_docs(self):
        """ check for method documentation """
        for func in dir(FileStorage):
            self.assertTrue(len(func.__doc__) > 0)


class TestPep8FileStorage(unittest.TestCase):
    """SI FUNCIONA
    check for pep8 validation """
    def test_pep8(self):
        """ test base and test_base for pep8 conformance """
        style = pep8.StyleGuide(quiet=True)
        file1 = 'models/engine/file_storage.py'
        file2 = 'tests/test_models/test_engine/test_file_storage.py'
        result = style.check_files([file1, file2])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warning).")


class TestFileStorage(unittest.TestCase):
    """Tests file_storage.py"""
    def setUp(self):
        """sets the start point"""
        pass

    def tearDown(self):
        """clean everything up after running setup"""
        sys.stdout = sys.__stdout__
        os.remove("file.json")

    def test_dicts(self):
        """tests dictionaries in the FileStorage"""
        storage = FileStorage()
        d = storage.all()
        self.assertIsInstance(d, dict)
        self.assertIs(d, storage._FileStorage__objects)

    def test_new(self):
        """tests if an object was created with an id"""
        storage = FileStorage()
        box = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        my_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                one_class = value()
                real_key = one_class.__class__.__name__ + "." + one_class.id
                storage.new(one_class)
                my_dict[real_key] = one_class
                self.assertEqual(my_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = box

    def test_save_and_reload(self):
        """tests if an object was serialized and if a string was
        deserialized"""
        storage = FileStorage()
        my_dict = {}
        for key, value in classes.items():
            one_class = value()
            real_key = one_class.__class__.__name__ + "." + one_class.id
            my_dict[real_key] = one_class
        box = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = my_dict
        storage.save()
        FileStorage._FileStorage__objects = box
        for key, value in my_dict.items():
            my_dict[key] = one_class.to_dict()
        string = json.dumps(my_dict)
        with open("file.json", "r") as my_file:
            item = my_file.read()
        self.assertEqual(json.loads(string), json.loads(item))
