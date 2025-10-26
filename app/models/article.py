from app.extensions import db
from sqlalchemy import Column, Date, Integer, Double, String, ForeignKey, Text, UniqueConstraint

class Article(db.Model):

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=False)
    price = Column(Double, nullable=False, unique=False)
    unit = Column(String(50), nullable=False, unique=False)
    lot = Column(String(50), nullable=True, unique=False)
    notes = Column(Text, nullable=True, unique=False, default=None)
    date = Column(Date, nullable=False, unique=False)
    # Foreign key to user id
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=False)

    # ORM relationships
    user = db.relationship('User', back_populates='articles')

    # Unique constraint to ensure two user can have the smae article name
    __table_args__ = (
        UniqueConstraint('user_id', 'name', 'date', name='_user_article_name_uc'), # means in a sale from a specific date can't repeat the same article name and client name
    )