from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from app.schemas.sale import *
from app.services.sale import *

sale_blp = Blueprint('Sale', 'sale', url_prefix='/sale', description='Sale related operations')

class SaleResource(MethodView):

    @sale_blp.route('/getAllSalesFromUser/<int:user_id>', methods=['GET'])
    @sale_blp.doc(params={'search': {'description': 'Search term', 'in': 'query', 'type': 'string', 'required': False},
                          'date': {'description': 'Date', 'in': 'query', 'type': 'string', 'required': False}})
    @jwt_required()
    @sale_blp.response(200, SaleOutputSchema(many=True))
    @sale_blp.doc(security=[{"bearerAuth": []}]) 
    def get_all_sales_from_user(user_id):
        """Get all articles of a user"""
        search = request.args.get('search', '')
        date = request.args.get('date','')
        return get_all_sales_from_user(user_id, search, date)
    
    @sale_blp.route('/getAllSalesFromArticle/<int:user_id>', methods=['GET'])
    @sale_blp.doc(params={'search': {'description': 'Search term', 'in': 'query', 'type': 'string', 'required': False},
                          'date': {'description': 'Date', 'in': 'query', 'type': 'string', 'required': False}})
    @jwt_required()
    @sale_blp.response(200, SaleOutputSchema(many=True))
    @sale_blp.doc(security=[{"bearerAuth": []}]) 
    def get_all_sales_from_article(user_id):
        """Get all articles of a user"""
        search = request.args.get('search', '')
        date = request.args.get('date','')
        return get_all_sales_from_article(user_id, search, date)
    
    @sale_blp.route('/create', methods=['POST'])
    @jwt_required()
    @sale_blp.arguments(SaleInputSchema)
    @sale_blp.response(201, SaleOutputSchema)
    @sale_blp.doc(security=[{"bearerAuth": []}])
    def post(sale):
        """Create a new article"""
        return create_sale(sale)
    
    @sale_blp.route('/get/<int:sale_id>', methods=['GET'])
    @jwt_required()
    @sale_blp.response(200, SaleOutputSchema)
    @sale_blp.doc(security=[{"bearerAuth": []}])
    def get(sale_id):
        """Get an article by id"""
        return get_sale(sale_id)
    
    @sale_blp.route('/update/<int:sale_id>', methods=['PUT'])
    @jwt_required()
    @sale_blp.arguments(SaleUpdateSchema)
    @sale_blp.response(200, SaleOutputSchema)
    @sale_blp.doc(security=[{"bearerAuth": []}])
    def put(sale, sale_id):
        """Update an article by id"""
        return update_sale(sale, sale_id)
    
    @sale_blp.route('/delete/<int:sale_id>', methods=['DELETE'])
    @jwt_required()
    @sale_blp.response(204)
    @sale_blp.doc(security=[{"bearerAuth": []}])
    def delete(sale_id):
        """Delete an article by id"""
        return delete_sale(sale_id)
    
