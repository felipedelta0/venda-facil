from flask import Blueprint, render_template
from app.services.report_service import generate_sales_report, get_all_products

report_routes = Blueprint("report_routes", __name__)


@report_routes.route("/reports")
def reports():
    chart_data = generate_sales_report()

    products = get_all_products()

    return render_template("report.html", chart_data=chart_data, products=products)
