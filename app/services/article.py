from app.models.article import Article
from app.models.sale import Sale
from app.extensions import db
from flask import abort

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

def duplicate_articles(date_to_insert, user_id):
    # Get the last day in the database with articles for the user
    last_day_result = db.session.query(Article.date).filter(Article.user_id == user_id).order_by(Article.date.desc()).first()
    if not last_day_result:
        return abort(404, description="No hay artículos para duplicar")

    last_day = last_day_result[0]

    # Get all articles from the last day
    articles_to_duplicate = Article.query.filter(Article.date == last_day, Article.user_id == user_id).all()
    if not articles_to_duplicate:
        return abort(404, description="No hay artículos para duplicar en la fecha proporcionada")

    duplicated_articles_list = []
    try:
        for article in articles_to_duplicate:
            # Check if an identical article already exists for the user, name, and current date_to_insert
            # This check is crucial to prevent re-inserting on retry after a partial failure
            exists = Article.query.filter_by(
                user_id=article.user_id,
                name=article.name,
                date=date_to_insert
            ).first()

            if exists:
                # If an article already exists (e.g., from a previous partial run that committed),
                # you might want to log this or decide how to handle it.
                # For a clean rollback, we generally want to avoid partial commits.
                # Since we are doing a single commit at the end, 'exists' here means
                # it exists from a *previous, completed transaction*.
                print(f"DEBUG: El artículo ya existe para el usuario {article.user_id}, nombre {article.name} y fecha {date_to_insert}. Saltando duplicación.")
                continue # Skip this article

            new_article = Article(
                name=article.name,
                price=article.price,
                unit=article.unit,
                lot=article.lot,
                user_id=article.user_id,
                date=date_to_insert
            )
            # Add the new article to the session. It's not yet committed to the DB.
            db.session.add(new_article)
            duplicated_articles_list.append(new_article)

        # If all additions were successful, commit the entire transaction
        db.session.commit()
        print(f"Duplicando artículos para user_id={user_id} en fecha={date_to_insert}: {[a.name for a in duplicated_articles_list]}")
        print("Commit realizado")
        return duplicated_articles_list

    except Exception as e:
        # If any error occurs during the process (e.g., a database constraint violation
        # not caught by your 'exists' check, or a network issue during commit)
        # then roll back all changes made in this session.
        db.session.rollback()
        print(f"ERROR: Fallo al duplicar artículos para user_id={user_id} en fecha={date_to_insert}. Se realizó un rollback: {e}")
        # Re-raise the exception or abort with a 500 status code
        # depending on how you want to handle internal errors.
        abort(500, description=f"Error al duplicar artículos: {e}")

def get_article(article_id):
        
        article = Article.query.get(article_id)
    
        if not article:
            return abort(404, description="El artículo no existe")
    
        return article

def update_article(article_data, article_id):
    article = Article.query.get(article_id)
    
    if not article:
        return abort(404, description="El artículo no existe")
    
    # Verify if the article is in a sale within the same date
    sales = Sale.query.filter_by(article_name=article.name, sale_date=article.date).all()
    
    # Updating the article data
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
    if 'notes' in article_data:
        article.notes = article_data['notes']
    
    try:
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


    


