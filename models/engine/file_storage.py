#!/usr/bin/env python3
"""File storage for hbnb clone."""
import json
import os
from importlib import import_module

class FileStorage:
    """Manages hbnb model storage in JSON format."""
    __file_path = 'file.json'
    __objects = {}

    def __init__(self):
        """Initialize a FileStorage instance."""
        self.model_classes = {
            'BaseModel': import_module('models.base_model').BaseModel,
            'User': import_module('models.user').User,
            'State': import_module('models.state').State,
            'City': import_module('models.city').City,
            'Amenity': import_module('models.amenity').Amenity,
            'Place': import_module('models.place').Place,
            'Review': import_module('models.review').Review
        }

    def all(self, MyClass=None):
        """Return a dictionary of stored models."""
        if MyClass is None: return self.__objects
        filtered_dict = {}
        for k, v in self.__objects.items():
            if type(v) is MyClass: filtered_dict[k] = v
        return filtered_dict

    def delete(self, obj=None):
        """Remove an object from storage."""
        if obj:
            key = obj.to_dict()['__class__'] + '.' + obj.id
            if key in self.__objects: del self.__objects[key]

    def new(self, obj):
        """Add a new object to storage."""
        self.__objects.update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Save storage to file."""
        with open(self.__file_path, 'w') as file:
            temp = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(temp, file)

    def reload(self):
        """Load storage from file."""
        classes = self.model_classes
        if os.path.isfile(self.__file_path):
            temp = {}
            with open(self.__file_path, 'r') as file:
                temp = json.load(file)
                for k, v in temp.items():
                    self.all()[k] = classes[v['__class__']](**v)

    def close(self):
        """Close the storage engine."""
        self.reload()

