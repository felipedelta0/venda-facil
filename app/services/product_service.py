from app.extensions import db
from app.models.product import Product
from flask import flash


def create_product(name, description, price, cost, stock, brand, size, category, color):
    if (
        not name
        or not price
        or not stock
        or not cost
        or not brand
        or not size
        or not category
        or not color
    ):
        flash("Preencha os campos obrigatórios!")
        return None

    try:
        price = float(price)
        cost = float(cost)
        stock = int(stock)
    except ValueError:
        flash("Preço, custo e estoque devem ser numéricos!")
        return None

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        cost=cost,
        brand=brand,
        size=size,
        category=category,
        color=color,
    )
    db.session.add(product)
    db.session.commit()
    flash("Produto cadastrado!")
    return product


def update_product(
    product, name, description, price, cost, stock, brand, size, category, color
):
    product.name = name or product.name
    product.description = description or product.description
    product.brand = brand or product.brand
    product.size = size or product.size
    product.category = category or product.category
    product.color = color or product.color

    if price:
        try:
            product.price = float(price)
        except ValueError:
            flash("Preço inválido!")
            return None

    if cost:
        try:
            product.cost = float(cost)
        except ValueError:
            flash("Custo inválido!")
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
