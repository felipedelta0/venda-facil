from flask import Flask
from .extensions import db
from .routes import main_routes, product_routes, sale_routes, report_routes


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sua_chave_secreta"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main_routes, url_prefix="/")
    app.register_blueprint(product_routes, url_prefix="/products")
    app.register_blueprint(sale_routes, url_prefix="/sales")
    app.register_blueprint(report_routes, url_prefix="/reports")

    return app

app = create_app()