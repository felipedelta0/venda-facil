from app.extensions import db
from app.models.sale import Sale
from app.models.product import Product
from sqlalchemy import func
import datetime
import pytz

def generate_sales_report():
    today = datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).date()

    start_date = today - datetime.timedelta(days=30)

    sales_data = (
        db.session.query(
            func.date_trunc('day', Sale.sale_date).label("day"),
            func.sum(Sale.quantity).label("total_quantity"),
            func.sum(Sale.total_price).label("total_value"),
        )
        .filter(Sale.sale_date >= start_date)
        .group_by(func.date_trunc('day', Sale.sale_date))
        .order_by(func.date_trunc('day', Sale.sale_date))
        .all()
    )

    chart_data = [
        {"day": day, "total_quantity": total_quantity, "total_value": total_value}
        for day, total_quantity, total_value in sales_data
    ]

    return chart_data


def get_all_products():
    return Product.query.all()
