from datetime import datetime

from app.extensions import db


class TransactionHeader(db.Model):
    __tablename__ = 'transaction_headers'

    id = db.Column(db.BigInteger, primary_key=True)
    added_date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    user = db.Column(db.Integer)

    details = db.relationship("TransactionDetail", back_populates="header")

class TransactionDetail(db.Model):
    __tablename__ = 'transaction_details'

    id = db.Column(db.BigInteger, primary_key=True)
    added_date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    id_header = db.Column(db.BigInteger, db.ForeignKey('transaction_headers.id'))
    header = db.relationship("TransactionHeader", back_populates="details")

    date = db.Column(db.DateTime)
    amount = db.Column(db.Numeric(18, 4))
    currency = db.Column(db.String(3))

    id_wallet = db.Column(db.BigInteger, db.ForeignKey('wallets.id'))
    wallet = db.relationship("Wallet", back_populates="transactions")

    # id_category
    # category
