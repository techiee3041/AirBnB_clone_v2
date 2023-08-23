#!/usr/bin/python3

import os
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base

class Amenity(BaseModel, Base):
    """Represents an amenity data set. Defines 'name' property based on storage type."""
    __tablename__ = 'amenities'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ''

