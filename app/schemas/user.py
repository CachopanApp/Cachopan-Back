from app.models.user import User
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class UserSchema(SQLAlchemyAutoSchema):
    class Meta: # This class is necessary to define the model to be serialized
        model = User
        exclude = ("id",)  # Excluir el campo 'id'

class UserTokenSchema(Schema):
    access_token = fields.String(required=True)
    refresh_token = fields.String(required=True)

class UserAccessSchema(Schema):
    access_token = fields.String(required=True)

class UserLoginSchema(Schema):
    name = fields.String(required=True)
    password = fields.String(required=True)