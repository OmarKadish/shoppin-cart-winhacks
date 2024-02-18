from config.init import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(60), nullable = False, unique = True)
    password_hash = db.Column(db.String(60), nullable = False)
    balance = db.Column(db.Float, nullable = False, default = 1000)
    cart_items = db.relationship('CartItem', backref = "buyer", lazy = True)
    def __repr__(self):
        return f"User(name='{self.name}', email='{self.email}', balance={self.balance})"
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.Text, nullable = True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return f"Item(name='{self.name}', price='{self.price}', buyer_id={self.buyer_id})"
    
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    quantity = db.Column(db.Integer, nullable = True)
    def __repr__(self):
        return f"CartItem(quantity='{self.quantity}')"
    
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    date = db.Column(db.DateTime, default = datetime.utcnow)
    total = db.Column(db.Float, nullable = False)
    def __repr__(self):
        return f"Transaction(user_id='{self.user_id}', date='{self.date}', total={self.total})"