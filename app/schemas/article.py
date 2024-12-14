from marshmallow import fields
from app.models.article import Article
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class ArticleInputSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        include_fk = True
        exclude = ("id",)

class ArticleOutputSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        include_fk = True

class ArticleUpdateSchema(SQLAlchemyAutoSchema):

    price = fields.Float(allow_none=True)

    class Meta:
        model = Article
        include_fk = True
        exclude = ("id", "user_id")