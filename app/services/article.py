from app.models.article import Article
from app.extensions import db
from flask import abort
import re

def get_all_articles(user_id, search):
    articles = Article.query.filter( Article.user_id == user_id, Article.name.ilike(f'%{search}%')).all() 
    return articles

def create_article(article):

    if article['name'] == "" or article['price'] == "" or article['unit'] == "" or article['user_id'] == "":
        return abort(400, description="Se han de rellenar todos los campos")
    
    if article['lot'] == "":
        article['lot'] = None

    new_article = Article(name=article['name'], price=article['price'], unit=article['unit'], lot=article['lot'], user_id=article['user_id'])

    if Article.query.filter_by(user_id=article['user_id'], name=article['name']).first():
        return abort(409, description="El artículo ya existe para ese usuario")
    
    db.session.add(new_article)
    db.session.commit()

    return new_article

def get_article(article_id):
        
        article = Article.query.get(article_id)
    
        if not article:
            return abort(404, description="El artículo no existe")
    
        return article

def update_article(article_data, article_id):

    article = Article.query.get(article_id)
    
    if not article:
        return abort(404, description="El artículo no existe")
    
    # Actualizar solo los campos que no son None
    if article_data.get('name') != "":
        article.name = article_data['name']
    if article_data.get('price') is not None:
        article.price = article_data['price']
    if article_data.get('unit') != "":
        article.unit = article_data['unit']
    if article_data.get('lot') != "":
        article.lot = article_data['lot']
    if article_data.get('user_id') is not None:
        article.user_id = article_data['user_id']
    
    # Guardar los cambios en la base de datos
    db.session.commit()
    
    return article

def delete_article(article_id):
        
    article = Article.query.get(article_id)
    
    if not article:
        return abort(404, description="El artículo no existe")
    
    db.session.delete(article)
    db.session.commit()
        
    return ('', 204)


    


