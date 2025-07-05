from app.models.sale import Sale
from app.models.article import Article
from app.extensions import db
from flask import abort

def get_all_sales_from_user(user_id, search, date):
    query = Sale.query.filter(Sale.user_id == user_id)
    
    if date:
        query = query.filter(Sale.sale_date == date)
    
    if search:
        query = query.filter(Sale.client_name.ilike(f'%{search}%'))
    
    sales = query.all()
    return sales

def get_all_sales_from_article(user_id, search, date):
    query = Sale.query.filter(Sale.user_id == user_id)
    
    if date:
        query = query.filter(Sale.sale_date == date)
    
    if search:
        query = query.filter(Sale.article_name.ilike(f'%{search}%'))
    
    sales = query.all()
    return sales

def create_sale(sale):
    
    if sale['user_id'] == "" or sale['sale_date'] == "" or sale['price_unit'] == "" or sale['article_name'] == "" \
        or sale['client_name'] == "" or sale['quantity'] == "":
        return abort(400, description="Se han de rellenar todos los campos")
    
    # Obtener la unidad del articulo

    article = Article.query.filter_by(user_id=sale['user_id'], name=sale['article_name']).first()
    if not article:
        return abort(404, description="El artículo no existe")
    
    total = round(sale['price_unit'] * sale['quantity'],2)
    
    new_sale = Sale(user_id=sale['user_id'], sale_date=sale['sale_date'], price_unit=sale['price_unit'],\
                     article_name=sale['article_name'], article_unit=article.unit, article_lot=sale['article_lot'], client_name=sale['client_name'], quantity=sale['quantity'], total=total)
    
    if Sale.query.filter_by(user_id=sale['user_id'], article_name=sale['article_name'], sale_date=sale['sale_date'], client_name=sale['client_name']).first():
        return abort(409, description="La venta ya existe para ese usuario")

    db.session.add(new_sale)
    db.session.commit()

    return new_sale

def get_sale(sale_id):
        
    sale = Sale.query.filter_by(id=sale_id).first()

    if not sale:
        return abort(404, description="La venta no existe")

    return sale

def update_sale(sale_data, sale_id):
    sale = Sale.query.filter_by(id=sale_id).first()
    
    if not sale:
        return abort(404, description="La venta no existe")
    
    if 'price_unit' in sale_data and sale_data['price_unit'] is not None:
        sale.price_unit = sale_data['price_unit']
    if 'quantity' in sale_data and sale_data['quantity'] is not None:
        sale.quantity = sale_data['quantity']

    # Recalcular el total si price_unit o quantity han cambiado
    if 'price_unit' in sale_data or 'quantity' in sale_data:
        sale.total = round(sale.price_unit * sale.quantity,2)
    
    db.session.commit()
    
    return sale

def delete_sale(sale_id):

    sale = Sale.query.filter_by(id=sale_id).first()
    
    if not sale:
        return abort(404, description="La venta no existe")
    
    db.session.delete(sale)
    db.session.commit()
        
    return (""), 204