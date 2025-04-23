from app.extensions import db
from app.models.product import Product
from app.models.sale import Sale
from sqlalchemy import func
import datetime
import pytz

def create_sale(product_id, quantity):
    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        return None, "Estoque insuficiente!"

    total_price = product.price * quantity
    sale_date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    sale = Sale(product_id=product.id, quantity=quantity, total_price=total_price, sale_date=sale_date)

    product.stock -= quantity
    db.session.add(sale)
    db.session.commit()

    return sale, None


def get_sales_summary(option, chosen_date_str):
    result = None
    sales = []

    if chosen_date_str:
        try:
            chosen_date = datetime.datetime.strptime(chosen_date_str, "%Y-%m-%d").date()
        except ValueError:
            return result, sales, "Data inválida!"

    else:
        chosen_date = None

    if option == "day_sales" and chosen_date:
        sales = Sale.query.filter(func.date(Sale.sale_date) == chosen_date_str).all()
    elif option == "day_total" and chosen_date:
        total_day = (
            db.session.query(func.sum(Sale.total_price))
            .filter(func.date(Sale.sale_date) == chosen_date_str)
            .scalar()
            or 0.0
        )
        result = total_day
    elif option == "week_total" and chosen_date:
        start_week = chosen_date - datetime.timedelta(days=chosen_date.weekday())
        end_week = start_week + datetime.timedelta(days=6)
        total_week = (
            db.session.query(func.sum(Sale.total_price))
            .filter(
                func.date(Sale.sale_date) >= start_week.isoformat(),
                func.date(Sale.sale_date) <= end_week.isoformat(),
            )
            .scalar()
            or 0.0
        )
        result = total_week
    elif option == "month_total" and chosen_date:
        month_str = chosen_date.strftime("%Y-%m")
        total_month = (
            db.session.query(func.sum(Sale.total_price))
            .filter(func.strftime("%Y-%m", Sale.sale_date) == month_str)
            .scalar()
            or 0.0
        )
        result = total_month
    elif option == "year_total" and chosen_date:
        year_str = chosen_date.strftime("%Y")
        total_year = (
            db.session.query(func.sum(Sale.total_price))
            .filter(func.strftime("%Y", Sale.sale_date) == year_str)
            .scalar()
            or 0.0
        )
        result = total_year
    elif option == "all_sales":
        sales = Sale.query.order_by(Sale.sale_date.asc()).all()

    return result, sales, None
