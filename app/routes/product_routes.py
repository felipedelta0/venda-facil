from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.product import Product

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/product/new', methods=['GET', 'POST'])
def new_product():
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')

        if not name or not price or not stock:
            flash("Preencha os campos obrigatórios!")
            return redirect(url_for('product_routes.new_product'))

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            flash("Preço e estoque devem ser numéricos!")
            return redirect(url_for('product_routes.new_product'))

        product = Product(name=name, description=description, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        flash("Produto cadastrado!")
        return redirect(url_for('main_routes.index'))

    return render_template('product_form.html', action="Novo Produto")

@product_routes.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        product.name = request.form.get('name', product.name)
        product.description = request.form.get('description', product.description)
        new_price = request.form.get('price')
        new_stock = request.form.get('stock')
        if new_price:
            try:
                product.price = float(new_price)
            except ValueError:
                flash("Preço inválido!")
                return redirect(url_for('product_routes.edit_product', product_id=product_id))
        if new_stock:
            try:
                product.stock = int(new_stock)
            except ValueError:
                flash("Estoque inválido!")
                return redirect(url_for('product_routes.edit_product', product_id=product_id))

        db.session.commit()
        flash("Produto atualizado!")
        return redirect(url_for('main_routes.index'))

    return render_template('product_form.html', action="Editar Produto", product=product)