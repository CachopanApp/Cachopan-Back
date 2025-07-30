from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from app.schemas.article import *
from app.services.article import *

article_blp = Blueprint('Article', 'article', url_prefix='/article', description='Article related operations')

class ArticleResource(MethodView):

    @article_blp.route('/getAll/<int:user_id>', methods=['GET'])
    @article_blp.doc(params={'search': {'description': 'Search term', 'in': 'query', 'type': 'string', 'required': False}})
    @jwt_required()
    @article_blp.response(200, ArticleOutputSchema(many=True))
    @article_blp.doc(security=[{"bearerAuth": []}]) 
    def get_all(user_id):
        """Get all articles of a user"""
        search = request.args.get('search', '')
        date = request.args.get('date','')
        return get_all_articles(user_id, search, date)
    
    @article_blp.route('/create', methods=['POST'])
    @jwt_required()
    @article_blp.arguments(ArticleInputSchema)
    @article_blp.response(201, ArticleOutputSchema)
    @article_blp.doc(security=[{"bearerAuth": []}])
    def post(article):
        """Create a new article"""
        return create_article(article)

    # Duplicate the articles from the last day with articles
    @article_blp.route('/duplicate', methods=['POST'])
    @jwt_required()
    @article_blp.response(201, ArticleOutputSchema(many=True))
    @article_blp.doc(security=[{"bearerAuth": []}])
    def duplicate():
        """Duplicate articles from the last day"""
        data = request.get_json()
        date_to_insert = data.get('date')
        user_id = data.get('user_id')
        return duplicate_articles(date_to_insert, user_id)
    
    @article_blp.route('/get/<int:article_id>', methods=['GET'])
    @jwt_required()
    @article_blp.response(200, ArticleOutputSchema)
    @article_blp.doc(security=[{"bearerAuth": []}])
    def get(article_id):
        """Get an article by id"""
        return get_article(article_id)      
    
    @article_blp.route('/update/<int:article_id>', methods=['PUT'])
    @jwt_required()
    @article_blp.arguments(ArticleUpdateSchema)
    @article_blp.response(200, ArticleOutputSchema)
    @article_blp.doc(security=[{"bearerAuth": []}])
    def put(article, article_id):
        """Update an article by id"""
        return update_article(article, article_id)
    
    @article_blp.route('/delete/<int:article_id>', methods=['DELETE'])
    @jwt_required()
    @article_blp.response(204)
    @article_blp.doc(security=[{"bearerAuth": []}])
    def delete(article_id):
        """Delete an article by id"""
        return delete_article(article_id)