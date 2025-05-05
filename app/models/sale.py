from sqlalchemy import func, Numeric
from decimal import Decimal
from app.extensions import db

import datetime
import pytz

class Sale(db.Model):
    __tablename__ = "sale"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    total_price = db.Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))

    product = db.relationship("Product", back_populates="sales")