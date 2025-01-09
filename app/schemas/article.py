from marshmallow import fields
from app.models.article import Article
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class ArticleInputSchema(SQLAlchemyAutoSchema):
    date = fields.Date(format='%d-%m-%Y')
    class Meta:
        model = Article
        include_fk = True
        exclude = ("id",)

class ArticleOutputSchema(SQLAlchemyAutoSchema):
    date = fields.Date(format='%d-%m-%Y')
    class Meta:
        model = Article
        include_fk = True

class ArticleUpdateSchema(SQLAlchemyAutoSchema):
    name = fields.String(allow_none=True)
    price = fields.Float(allow_none=True)
    unit = fields.String(allow_none=True)
    lot = fields.String(allow_none=True)
    user_id = fields.Integer(allow_none=True)

    class Meta:
        model = Article
        include_fk = True
        exclude = ("id", "date")