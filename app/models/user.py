from app.extensions import db
from sqlalchemy import Column, Integer, String
from .client import Client

class User(db.Model):

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=True, unique=True)
    password = Column(String, nullable=False)

    # ORM relationships
    clients = db.relationship('Client', back_populates='user', cascade='all, delete-orphan')
