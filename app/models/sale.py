from app.extensions import db
import datetime
import pytz


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    #sale_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    sale_date = db.Column(db.DateTime, default=datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
    total_price = db.Column(db.Float, nullable=False, default=0.0)
    product = db.relationship("Product", backref=db.backref("sales", lazy=True))
