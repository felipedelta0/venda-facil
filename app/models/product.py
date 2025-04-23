from app.extensions import db
import datetime
import pytz


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    cost = db.Column(db.Float, nullable=False, default=0.0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    #created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
