from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    item = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name,
                'items': [item.json for item in self.item.all()]}

    @classmethod
    def find_by_name(cls, name):
        # equivalent to: SELECT * FROM items WHERE name=name LIMIT 1
        # filter_by can take more than one arg e.g. filter_by(name=name, id=1)
        return cls.query.filter_by(name=name).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        return([val.name for val in cls.query.all()])
