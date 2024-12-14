from app.extensions import db
from sqlalchemy import Column, Date, Integer, Double, String, ForeignKey, UniqueConstraint

class Sale(db.Model):

    id = Column(Integer, autoincrement=True, primary_key=True)
    sale_date = Column(Date , primary_key=True)
    article_name = Column(String(50), nullable=False, unique=False)
    client_name = Column(String(50), nullable=False, unique=False)
    price_unit = Column(Double, nullable=False, unique=False)
    quantity = Column(Integer, nullable=False, unique=False)
    total = Column(Double, nullable=False, unique=False)
    # Foreign key to user id
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=False)

    # ORM relationships
    user = db.relationship('User', back_populates='sales')

    # Unique constraint to ensure two user can have the smae article name
    __table_args__ = (
        UniqueConstraint('user_id', 'sale_date', 'article_name', 'client_name', name='_user_sale_name_uc'), # means in a sale from a specific date can't repeart the same article name and client name
    )