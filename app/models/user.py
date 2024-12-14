from app.extensions import db
from sqlalchemy import Column, Integer, String
from .client import Client
from .article import Article
from .sale import Sale

class User(db.Model):

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=True, unique=True)
    password = Column(String, nullable=False)

    # ORM relationships
    clients = db.relationship('Client', back_populates='user', cascade='all, delete-orphan')
    articles = db.relationship('Article', back_populates='user', cascade='all, delete-orphan')
    sales = db.relationship('Sale', back_populates='user', cascade='all, delete-orphan')
