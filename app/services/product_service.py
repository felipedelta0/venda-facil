from app.extensions import db
from app.models.product import Product
from flask import flash


def create_product(name, description, price, stock):
    if not name or not price or not stock:
        flash("Preencha os campos obrigatórios!")
        return None

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        flash("Preço e estoque devem ser numéricos!")
        return None

    product = Product(name=name, description=description, price=price, stock=stock)
    db.session.add(product)
    db.session.commit()
    flash("Produto cadastrado!")
    return product


def update_product(product, name, description, price, stock):
    product.name = name or product.name
    product.description = description or product.description

    if price:
        try:
            product.price = float(price)
        except ValueError:
            flash("Preço inválido!")
            return None

    if stock:
        try:
            product.stock = int(stock)
        except ValueError:
            flash("Estoque inválido!")
            return None

    db.session.commit()
    flash("Produto atualizado!")
    return product
