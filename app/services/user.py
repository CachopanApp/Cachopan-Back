from app.models.user import User
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token
from flask import abort
import re

def create_user(data):

    regex_password = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    regex_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not data['name'] or not data['password'] or not data['email']:
        return abort(400, description="No se permiten campos vacíos")

    if not re.match(regex_password, data['password']):
        return abort(400, description="La contraseña debe tener al menos 8 caracteres, una letra, un número y un caracter especial")
    
    if not re.match(regex_email, data['email']):
        return abort(400, description="El email no es válido")

    if User.query.filter_by(name=data['name']).first():
        return abort(409, description="El nombre de usuario ya existe")
    
    if User.query.filter_by(email=data['email']).first():
        return abort(409, description="El email ya existe")
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def authenticate_user(data):
    
    user = User.query.filter_by(name=data['name']).first()

    if not user:
        return abort(404, description="The user does not exist")

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token}
    
    return abort(401, description="Invalid credentials")