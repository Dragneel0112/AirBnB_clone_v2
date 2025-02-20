#!/usr/bin/python3
""" Class to manage file storage for AirBnB clone """
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """ Class manages storage of AirBnB models in JSON format """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """ Returns a dictionary of models currently in storage """
        if cls:
            if type(cls) == str:
                cls = classes[cls]

            class_name = cls.__name__
            new_dict = {k: v for (k, v) in FileStorage.__objects.items()
                        if class_name in k}
            return new_dict
        else:
            return FileStorage.__objects

    def new(self, obj):
        """ Adds new object to storage dictionary """
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """ Saves storage dictionary to file """
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """ Loads storage dictionary from file """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Public instance method to delete obj from __objects
        if available
        """
        if obj:
            key = obj.__class__.__name__ + "." + obj.id
            self.all().pop(key)

    def close(self):
        """ Public method to call reload for deserializing the
        JSON file.
        """
        self.reload()
