from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from app.schemas.client import *
from app.services.client import *

client_blp = Blueprint('Client', 'client', url_prefix='/clients', description='Client related operations')

class ClientResource(MethodView):

    @client_blp.route('', methods=['GET'])
    @client_blp.doc(params=
        {'search': {'description': 'Search term', 'in': 'query', 'type': 'string', 'required': False},
         'user_id': {'description': 'User ID to filter clients', 'in': 'query', 'type': 'integer', 'required': True}}
    )
    @jwt_required()
    @client_blp.response(200, ClientOutputSchema(many=True))
    @client_blp.doc(security=[{"bearerAuth": []}])
    def get_all():
        """Get all clients of a user"""
        user_id = request.args.get('user_id', type=int)
        search = request.args.get('search', '')
        return get_all_clients(user_id, search)


    @client_blp.route('', methods=['POST'])
    @jwt_required()
    @client_blp.arguments(ClientInputSchema)
    @client_blp.response(201, ClientOutputSchema)
    @client_blp.doc(security=[{"bearerAuth": []}])
    def post(client):
        """Create a new client"""
        return create_client(client)
    
    @client_blp.route('/<int:client_id>', methods=['GET'])
    @jwt_required()
    @client_blp.response(200, ClientOutputSchema)
    @client_blp.doc(security=[{"bearerAuth": []}])
    def get(client_id):
        """Get a client by id"""
        return get_client(client_id)
    
    @client_blp.route('/<int:client_id>', methods=['PUT'])
    @jwt_required()
    @client_blp.arguments(ClientUpdateSchema)
    @client_blp.response(200, ClientOutputSchema)
    @client_blp.doc(security=[{"bearerAuth": []}])
    def put(client, client_id):
        """Update a client by id"""
        return update_client(client, client_id)
    
    @client_blp.route('/<int:client_id>', methods=['DELETE'])
    @jwt_required()
    @client_blp.response(204)
    @client_blp.doc(security=[{"bearerAuth": []}])
    def delete(client_id):
        """Delete a client by id"""
        return delete_client(client_id)