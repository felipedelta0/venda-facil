from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.sale_service import create_sale, get_sales_summary
from app.models.product import Product
import datetime

sale_routes = Blueprint('sale_routes', __name__)

@sale_routes.route('/sale/new', methods=['GET', 'POST'])
def new_sale():
    products = Product.query.all()
    if request.method == "POST":
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')

        if not product_id or not quantity:
            flash("Selecione um produto e informe a quantidade!")
            return redirect(url_for('sale_routes.new_sale'))

        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except ValueError:
            flash("Dados inválidos!")
            return redirect(url_for('sale_routes.new_sale'))

        sale, error_message = create_sale(product_id, quantity)
        if error_message:
            flash(error_message)
            return redirect(url_for('sale_routes.new_sale'))

        flash("Venda registrada!")
        return redirect(url_for('main_routes.index'))

    return render_template('sale_form.html', products=products)

@sale_routes.route('/sales_summary', methods=['GET'])
def sales_summary():
    option = request.args.get('option', 'all_sales')
    chosen_date_str = request.args.get('date')

    result, sales, error_message = get_sales_summary(option, chosen_date_str)

    if error_message:
        flash(error_message)

    return render_template('sales_summary.html', option=option, date=chosen_date_str, result=result, sales=sales)
