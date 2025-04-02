from flask import Blueprint, render_template
from app.models.product import Product

main_routes = Blueprint("main_routes", __name__)


@main_routes.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)
