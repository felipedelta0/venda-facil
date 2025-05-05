from app.extensions import db
from sqlalchemy import func, Numeric
from decimal import Decimal

import datetime
import pytz


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    cost = db.Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    price = db.Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    sales = db.relationship("Sale", back_populates="product")