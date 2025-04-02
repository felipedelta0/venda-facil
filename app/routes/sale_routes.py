from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.product import Product
from app.models.sale import Sale

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

        product = Product.query.get_or_404(product_id)
        if product.stock < quantity:
            flash("Estoque insuficiente!")
            return redirect(url_for('sale_routes.new_sale'))

        total_price = product.price * quantity
        sale = Sale(product_id=product.id, quantity=quantity, total_price=total_price)
        product.stock -= quantity
        db.session.add(sale)
        db.session.commit()
        flash("Venda registrada!")
        return redirect(url_for('main_routes.index'))

    return render_template('sale_form.html', products=products)

@sale_routes.route('/sales_summary', methods=['GET'])
def sales_summary():
    # Recupera os parâmetros da query string (ou define valores padrão)
    option = request.args.get('option', 'all_sales')
    chosen_date_str = request.args.get('date')  # formato 'YYYY-MM-DD'

    result = None  # Para valores acumulados
    sales = []  # Para quando quisermos a listagem de vendas

    # Se a opção for baseada em data e a data foi informada, podemos converter:
    if chosen_date_str:
        try:
            chosen_date = datetime.datetime.strptime(chosen_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Data inválida!")
            return render_template('sales_summary.html', option=option, date=chosen_date_str, result=result,
                                   sales=sales)
    else:
        chosen_date = None

    # Tratamento das opções:
    if option == 'day_sales' and chosen_date:
        # Exibe todas as vendas do dia escolhido
        sales = Sale.query.filter(func.date(Sale.sale_date) == chosen_date_str).all()
    elif option == 'day_total' and chosen_date:
        # Acumulado de vendas do dia escolhido
        total_day = db.session.query(func.sum(Sale.total_price)).filter(
            func.date(Sale.sale_date) == chosen_date_str).scalar() or 0.0
        result = total_day
    elif option == 'week_total' and chosen_date:
        # Calcula o intervalo da semana (supondo que a semana começa na segunda)
        start_week = chosen_date - datetime.timedelta(days=chosen_date.weekday())
        end_week = start_week + datetime.timedelta(days=6)
        total_week = db.session.query(func.sum(Sale.total_price)).filter(
            func.date(Sale.sale_date) >= start_week.isoformat(),
            func.date(Sale.sale_date) <= end_week.isoformat()
        ).scalar() or 0.0
        result = total_week
    elif option == 'month_total' and chosen_date:
        # Acumulado do mês: usa strftime para extrair ano-mês
        month_str = chosen_date.strftime('%Y-%m')
        total_month = db.session.query(func.sum(Sale.total_price)).filter(
            func.strftime('%Y-%m', Sale.sale_date) == month_str
        ).scalar() or 0.0
        result = total_month
    elif option == 'year_total' and chosen_date:
        # Acumulado do ano
        year_str = chosen_date.strftime('%Y')
        total_year = db.session.query(func.sum(Sale.total_price)).filter(
            func.strftime('%Y', Sale.sale_date) == year_str
        ).scalar() or 0.0
        result = total_year
    elif option == 'all_sales':
        # Lista de todas as vendas realizadas
        sales = Sale.query.order_by(Sale.sale_date.asc()).all()

    return render_template('sales_summary.html', option=option, date=chosen_date_str, result=result, sales=sales)