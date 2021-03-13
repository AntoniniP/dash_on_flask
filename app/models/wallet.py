from datetime import datetime

from app.extensions import db


class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.BigInteger, primary_key=True)
    added_date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    description = db.Column(db.String(255))
    initial_balance = db.Column(db.Numeric(18,4))
    default_currency = db.Column(db.String(3))
    user = db.Column(db.Integer)

    transactions = db.relationship("TransactionDetail", back_populates="wallet")
