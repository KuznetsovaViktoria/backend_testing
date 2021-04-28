from db import db

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Item %r>' % self.name

    @staticmethod
    def get(name):
        item = Item.query.filter_by(name=name).first()
        return item

    @staticmethod
    def get_all():
        items = Item.query.all()
        return items

    @staticmethod
    def post(name, price):
        db.session.add(Item(name=name, price=price))
        db.session.commit()

    @staticmethod
    def delete(name):
        item = Item.get(name)
        db.session.delete(item)
        db.session.commit()

    def jsoning(self):
        self.json = {'name': self.name, 'price': self.price}
