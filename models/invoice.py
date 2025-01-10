from utils.database import db
from datetime import datetime 


class Invoice(db.Model):

    invoice_id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.Integer, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    iva = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    total_with_iva = db.Column(db.Float, nullable=False)
     
    items = db.relationship('InvoiceItem', backref='invoice', cascade="all, delete-orphan", lazy=True)


def __repr__(self):
        return f"<Invoice {self.invoice_id} - Client {self.client_id}>"
    