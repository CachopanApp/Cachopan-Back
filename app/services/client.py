from app.models.client import Client
from app.extensions import db
from flask import abort
import re

def get_all_clients(user_id, search):
    # Clients with name like search
    clients = Client.query.filter(Client.user_id == user_id, Client.name.ilike(f'%{search}%')).all()
    return clients

def create_client(client):

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    number_regex = r'^[0-9]+$'

    if client['email'] == "":
        client['email'] = None
    elif not (re.match(email_regex, client['email'])):
        return abort(400, description="El email no es válido")
    
    if client['number'] == "":
        client['number'] = None 
    elif not re.match(number_regex, client['number']):
        return abort(400, description="El número no es válido")
    
    new_client = Client(name=client['name'], email=client['email'], number=client['number'], user_id=client['user_id'])
    
    if Client.query.filter_by(user_id=client['user_id'], name=client['name']).first():
        return abort(409, description="El cliente ya existe para ese usuario")
    
    if client['email'] and Client.query.filter_by(user_id=client['user_id'], email=client['email']).first():
        return abort(409, description="El email ya existe para ese usuario")

    if client['number'] and Client.query.filter_by(user_id=client['user_id'], number=client['number']).first():
        return abort(409, description="El número ya existe para ese usuario")  
    
    db.session.add(new_client)
    db.session.commit()

    return new_client

def get_client(client_id):
    
    client = Client.query.get(client_id)

    if not client:
        return abort(404, description="El cliente no existe")

    return client

def update_client(client, client_id):

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    number_regex = r'^[0-9]+$'

    if client['email'] == "":
        client['email'] = None
    elif not (re.match(email_regex, client['email'])):
        return abort(400, description="El email no es válido")
    
    if client['number'] == "":
        client['number'] = None 
    elif not re.match(number_regex, client['number']):
        return abort(400, description="El número no es válido")
    
    client_to_update = Client.query.get(client_id)

    if not client_to_update:
        return abort(404, description="El cliente no existe")
    
    if client['name'] != client_to_update.name and Client.query.filter_by(user_id=client_to_update.user_id, name=client['name']).first():
        return abort(409, description="El cliente ya existe para ese usuario")
    
    if client['email'] and client['email'] != client_to_update.email and Client.query.filter_by(user_id=client_to_update.user_id, email=client['email']).first():
        return abort(409, description="El email ya existe para ese usuario")

    if client['number'] and client['number'] != client_to_update.number and Client.query.filter_by(user_id=client_to_update.user_id, number=client['number']).first():
        return abort(409, description="El número ya existe para ese usuario")  

    if (client['name'] is not None): client_to_update.name = client['name']
    if (client['email'] is not None): client_to_update.email = client['email']
    if (client['number'] is not None): client_to_update.number = client['number']

    db.session.commit()

    return client_to_update

def delete_client(client_id):

    client = Client.query.get(client_id)

    if not client:
        return abort(404, description="El cliente no existe")
    
    db.session.delete(client)
    db.session.commit()

    return ('', 204)