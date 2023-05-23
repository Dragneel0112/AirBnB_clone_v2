#!/usr/bin/python3
""" Creates class Amenities for AirBnB console_v2 """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class Amenity(BaseModel, Base):
    """ Amenity class that inherits from BaseModel and Base """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        place_amenities = relationship("Place", secondary=place_amenity)
