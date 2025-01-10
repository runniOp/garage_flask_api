from utils.database import db

class InvoiceItem(db.Model):
   
    item_id = db.Column(db.Integer, primary_key=True)
    
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    task_id = db.Column(db.Integer, nullable=False)

    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.invoice_id'), nullable=False)


def __repr__(self):
        return f"<InvoiceItem {self.item_id} - {self.description} (${self.cost})>"