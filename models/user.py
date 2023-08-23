#!/usr/bin/python3

import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class User(BaseModel, Base):
    """User class with various attributes."""
    __tablename__ = 'users'
    
    # Define attributes based on storage type
    email = Column(String(128), nullable=False) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    password = Column(String(128), nullable=False) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    first_name = Column(String(128), nullable=True) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    last_name = Column(String(128), nullable=True) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    
    # Define relationships based on storage type
    places = relationship('Place', cascade="all, delete, delete-orphan", backref='user') if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    reviews = relationship('Review', cascade="all, delete, delete-orphan", backref='user') if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None

