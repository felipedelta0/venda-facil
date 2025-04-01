from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
# Configurando o SQLite
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "store.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# MODELOS
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False, default=0.0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False, default=0.0)
    product = db.relationship('Product', backref=db.backref('sales', lazy=True))


with app.app_context():
    db.create_all()


# ROTAS

# Página inicial – lista os produtos com seus estoques
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


# Cadastro de produto
@app.route('/product/new', methods=['GET', 'POST'])
def new_product():
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')

        if not name or not price or not stock:
            flash("Por favor, preencha os campos obrigatórios!")
            return redirect(url_for('new_product'))
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            flash("Preço deve ser numérico e estoque um valor inteiro!")
            return redirect(url_for('new_product'))

        product = Product(name=name, description=description, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        flash("Produto cadastrado com sucesso!")
        return redirect(url_for('index'))

    return render_template('product_form.html', action="Novo Produto")


# Atualização de produto (editar dados e estoque)
@app.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
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
                return redirect(url_for('edit_product', product_id=product_id))
        if new_stock:
            try:
                product.stock = int(new_stock)
            except ValueError:
                flash("Estoque inválido!")
                return redirect(url_for('edit_product', product_id=product_id))

        db.session.commit()
        flash("Produto atualizado!")
        return redirect(url_for('index'))

    return render_template('product_form.html', action="Editar Produto", product=product)


# Registro de venda – a venda atualiza automaticamente o estoque
@app.route('/sale/new', methods=['GET', 'POST'])
def new_sale():
    products = Product.query.all()
    if request.method == "POST":
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        if not product_id or not quantity:
            flash("Selecione um produto e informe a quantidade!")
            return redirect(url_for('new_sale'))
        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except ValueError:
            flash("Dados inválidos!")
            return redirect(url_for('new_sale'))
        product = Product.query.get_or_404(product_id)
        if product.stock < quantity:
            flash("Estoque insuficiente!")
            return redirect(url_for('new_sale'))

        total_price = product.price * quantity
        sale = Sale(product_id=product.id, quantity=quantity, total_price=total_price)
        product.stock -= quantity  # Atualiza o estoque
        db.session.add(sale)
        db.session.commit()
        flash("Venda registrada com sucesso!")
        return redirect(url_for('index'))

    return render_template('sale_form.html', products=products)


# Relatórios – gráficos temporais de vendas e visualização de estoque
@app.route('/reports')
def reports():
    # Agregando vendas dos últimos 30 dias
    today = datetime.datetime.utcnow().date()
    start_date = today - datetime.timedelta(days=30)
    sales_data = db.session.query(
        func.strftime('%Y-%m-%d', Sale.sale_date).label('day'),
        func.sum(Sale.quantity).label('total_quantity'),
        func.sum(Sale.total_price).label('total_value')
    ).filter(Sale.sale_date >= start_date) \
        .group_by('day') \
        .order_by('day').all()

    # Formatando os dados para o gráfico
    chart_data = [{'day': day, 'total_quantity': total_quantity, 'total_value': total_value}
                  for day, total_quantity, total_value in sales_data]
    products = Product.query.all()
    return render_template('report.html', chart_data=chart_data, products=products)


# Nova rota para exibir o resumo das vendas
@app.route('/sales_summary', methods=['GET'])
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


if __name__ == '__main__':
    app.run(debug=True)
