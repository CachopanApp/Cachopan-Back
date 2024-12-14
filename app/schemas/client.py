from app.models.client import Client
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class ClientInputSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        include_fk = True  
        exclude = ("id",)  # Excluir los campos 'id' en el esquema de entrada

class ClientOutputSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        include_fk = True

class ClientUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        include_fk = True
        exclude = ("id", "user_id")  # Excluir los campos 'id' y 'user_id' en el esquema de actualización