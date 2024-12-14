from app.models.sale import Sale
from app.extensions import db
from flask import abort
import re

def get_all_sales_from_user(user_id):
    sales = Sale.query.filter_by(user_id=user_id).all()
    return sales

def get_all_sales_from_user_date(user_id, date):
    sales = Sale.query.filter_by(user_id=user_id, sale_date=date).all()
    return sales

def create_sale(sale):
    
    if sale['user_id'] == "" or sale['sale_date'] == "" or sale['price_unit'] == "" or sale['article_name'] == "" \
        or sale['client_name'] == "" or sale['quantity'] == "" or sale['total'] == "":
        return abort(400, description="Se han de rellenar todos los campos")
    
    new_sale = Sale(user_id=sale['user_id'], sale_date=sale['sale_date'], price_unit=sale['price_unit'],\
                     article_name=sale['article_name'], client_name=sale['client_name'], quantity=sale['quantity'], total=sale['total'])
    
    if Sale.query.filter_by(user_id=sale['user_id'], article_name=sale['article_name'], sale_date=sale['sale_date']).first():
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
    
    # Actualizar solo los campos que no son None o vacíos
    if 'sale_date' in sale_data and sale_data['sale_date'] is not None:
        sale.sale_date = sale_data['sale_date']
    if 'price_unit' in sale_data and sale_data['price_unit'] is not None:
        sale.price_unit = sale_data['price_unit']
    if 'article_name' in sale_data and sale_data['article_name'] != "":
        sale.article_name = sale_data['article_name']
    if 'client_name' in sale_data and sale_data['client_name'] != "":
        sale.client_name = sale_data['client_name']
    if 'quantity' in sale_data and sale_data['quantity'] is not None:
        sale.quantity = sale_data['quantity']
    if 'total' in sale_data and sale_data['total'] is not None:
        sale.total = sale_data['total']
    
    db.session.commit()
    
    return sale

def delete_sale(sale_id):

    sale = Sale.query.filter_by(id=sale_id).first()
    
    if not sale:
        return abort(404, description="La venta no existe")
    
    db.session.delete(sale)
    db.session.commit()
        
    return (""), 204