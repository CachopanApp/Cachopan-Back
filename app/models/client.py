from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint

class Client(db.Model):

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=False)
    email = Column(String(50), nullable=True, unique=False)
    number = Column(String(50), nullable=True, unique=False)
    # Foreign key to user id
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=False)

    # ORM relationships
    user = db.relationship('User', back_populates='clients')

    # Unique constraint to ensure a user cannot have two clients with the same name, email, or number
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='_user_client_name_uc'),
        UniqueConstraint('user_id', 'email', name='_user_client_email_uc'),
        UniqueConstraint('user_id', 'number', name='_user_client_number_uc'),
    )