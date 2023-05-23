#!/usr/bin/python3
""" Creates class Place for AirBnB console_v2 """
import models
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import os


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ Class Place and information regarding the venue """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref='place',
                               cascade="all, delete")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """ Getter attribute reviews
            Returns the list of Reviews with place_id equals current Place.id
            """
            my_list = []
            extracted_reviews = models.storage.all('Review').values()
            for review in extracted_reviews:
                if self.id == review.place_id:
                    my_list.append(review)
            return my_list

        @property
        def amenities(self):
            """ Getter attribute amenities
            Returns the list of Amenities where amenity_ids
            contain Amenity.id linked to the Place.
            """
            my_list = []
            extracted_amenities = models.storage.all('Amenity').values()
            for amenity in extracted_amenities:
                if self.id == amenity.amenity_ids:
                    my_list.append(amenity)
            return my_list

        @amenities.setter
        def amenities(self, obj):
            """ Setter attribute an append method for adding an Amenity.id
            to the attribute amenity_ids.
            """
            if obj.__class__.__name__ == "Amenity":
                self.amenity_ids.append(obj.id)
