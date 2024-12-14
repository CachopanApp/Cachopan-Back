from marshmallow import fields
from app.models.sale import Sale
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class SaleInputSchema(SQLAlchemyAutoSchema):
    sale_date = fields.Date(format='%d-%m-%Y')
    class Meta:
        model = Sale
        include_fk = True
        exclude = ("id",)

class SaleOutputSchema(SQLAlchemyAutoSchema):
    sale_date = fields.Date(format='%d-%m-%Y')
    class Meta:
        model = Sale
        include_fk = True

class SaleUpdateSchema(SQLAlchemyAutoSchema):
    sale_date = fields.Date(format='%d-%m-%Y', allow_none=True)

    price_unit = fields.Float(allow_none=True)
    quantity = fields.Integer(allow_none=True)
    total = fields.Float(allow_none=True)

    class Meta:
        model = Sale
        include_fk = True
        exclude = ("id", "user_id")