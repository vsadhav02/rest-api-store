from db import db

"""
store and item table are linked to each other with store id.
Thats why we use relationship method here.
"""


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    items = db.relationship('ItemModel', lazy='dynamic')

    # above three parameter names should match exactly in order in below call to contsructor.
    # If not , your db will have above column name but values mis aligned.
    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
