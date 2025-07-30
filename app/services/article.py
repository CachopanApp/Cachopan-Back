from app.models.article import Article
from app.models.sale import Sale
from app.extensions import db
from flask import abort
import re

def get_all_articles(user_id, search, date):
    query = Article.query.filter(Article.user_id == user_id)
    
    if date:
        query = query.filter(Article.date == date)
    
    if search:
        query = query.filter(Article.name.ilike(f'%{search}%'))
    
    articles = query.all()

    return articles

def create_article(article):

    if article['name'] == "" or article['price'] == "" or article['unit'] == "" or article['user_id'] == "" or article['date'] == "":
        return abort(400, description="Se han de rellenar todos los campos")
    

    new_article = Article(name=article['name'], price=article['price'], unit=article['unit'], lot=article['lot'], user_id=article['user_id'], date = article['date'])

    if Article.query.filter_by(user_id=article['user_id'], name=article['name'], date=article['date'] ).first():
        return abort(409, description="El artículo ya existe para ese usuario")
    
    db.session.add(new_article)
    db.session.commit()

    return new_article

# Duplicate the articles from the last day with articles
def duplicate_articles(date_to_insert, user_id):

    # Get the last day in the database with articles for the user
    last_day = db.session.query(Article.date).filter(Article.user_id == user_id).order_by(Article.date.desc()).first()
    if not last_day:
        return abort(404, description="No hay artículos para duplicar")
    
    last_day = last_day[0]
    # Get all articles from the last day
    articles = Article.query.filter(Article.date == last_day, Article.user_id == user_id).all()

    # Duplicate the articles
    duplicated_articles = []
    for article in articles:
        # Verificar si ya existe un artículo igual para el usuario, nombre y fecha actual
        exists = Article.query.filter_by(
            user_id=article.user_id,
            name=article.name,
            date= date_to_insert
        ).first()
        if exists:
            continue  

        new_article = Article(
            name=article.name,
            price=article.price,
            unit=article.unit,
            lot=article.lot,
            user_id=article.user_id,
            date= date_to_insert
        )
        db.session.add(new_article)
        duplicated_articles.append(new_article)

    db.session.commit()
    return duplicated_articles

def get_article(article_id):
        
        article = Article.query.get(article_id)
    
        if not article:
            return abort(404, description="El artículo no existe")
    
        return article

def update_article(article_data, article_id):
    article = Article.query.get(article_id)
    
    if not article:
        return abort(404, description="El artículo no existe")
    
    # Verificar si el artículo está en una venta con el mismo nombre
    sales = Sale.query.filter_by(article_name=article.name).all()
    
    # Actualizar los atributos del artículo
    if 'name' in article_data and article_data['name']:
        article.name = article_data['name']
        for sale in sales:
            sale.article_name = article_data['name']
    if 'unit' in article_data and article_data['unit']:
        article.unit = article_data['unit']
        for sale in sales:
            sale.article_unit = article_data['unit']
    if 'price' in article_data and article_data['price']:
        for sale in sales:
            if sale.price_unit == article.price:
                sale.price_unit = article_data['price']
                quantity = sale.quantity
                sale.total = article_data['price'] * quantity
                
        article.price = article_data['price']
        

    if 'lot' in article_data and article_data['lot']:
        article.lot = article_data['lot']
        for sale in sales:
            sale.article_lot = article_data['lot']
    if 'user_id' in article_data and article_data['user_id'] is not None:
        article.user_id = article_data['user_id']
    
    try:
        # Guardar los cambios en la base de datos
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return abort(500, description="Error al actualizar el artículo")
    
    return article

def delete_article(article_id):
        
    article = Article.query.get(article_id)
    
    if not article:
        return abort(404, description="El artículo no existe")
    
    db.session.delete(article)
    db.session.commit()
        
    return ('', 204)


    


