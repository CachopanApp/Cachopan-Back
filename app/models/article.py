from app.extensions import db
from sqlalchemy import Column, Integer, Double, String, ForeignKey, UniqueConstraint

class Article(db.Model):

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=False)
    price = Column(Double, nullable=False, unique=False)
    unit = Column(String(50), nullable=False, unique=False)
    lot = Column(String(50), nullable=False, unique=False)
    # Foreign key to user id
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=False)

    # ORM relationships
    user = db.relationship('User', back_populates='articles')

    # Unique constraint to ensure two user can have the smae article name
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='_user_article_name_uc'), # means user_id and name must be unique
    )