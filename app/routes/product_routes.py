from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.product_service import create_product, update_product
from app.models.product import Product

product_routes = Blueprint("product_routes", __name__)


@product_routes.route("/product/new", methods=["GET", "POST"])
def new_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        cost = request.form.get("cost")
        stock = request.form.get("stock")
        brand = request.form.get("brand")
        size = request.form.get("size")
        category = request.form.get("category")
        color = request.form.get("color")

        # Chamar o serviço para criar o produto
        product = create_product(
            name, description, price, cost, stock, brand, size, category, color
        )

        if product is None:  # Caso tenha ocorrido erro
            return redirect(url_for("product_routes.new_product"))

        return redirect(url_for("main_routes.index"))

    return render_template("product_form.html", action="Novo Produto")


@product_routes.route("/product/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        cost = request.form.get("cost")
        stock = request.form.get("stock")
        brand = request.form.get("brand")
        size = request.form.get("size")
        category = request.form.get("category")
        color = request.form.get("color")

        # Chamar o serviço para atualizar o produto
        updated_product = update_product(
            product, name, description, price, cost, stock, brand, size, category, color
        )

        if updated_product is None:  # Caso tenha ocorrido erro
            return redirect(
                url_for("product_routes.edit_product", product_id=product_id)
            )

        return redirect(url_for("main_routes.index"))

    return render_template(
        "product_form.html", action="Editar Produto", product=product
    )
