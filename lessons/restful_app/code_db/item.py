import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


def return_item(name, items):
    return next(filter(lambda x: x['name'] == name, items), None)


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field can\'t be left blank')

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()
        return row

    @jwt_required()
    def get(self, name):
        row = self.find_by_name(name)
        if row:
            return {'item': {name: row[0], 'price': row[1]}}, 200
        return {'message': 'item not found'}, 404

    @jwt_required()
    def post(self, name):
        row = self.find_by_name(name)
        if row:
            return {'message': 'item exists'}, 404

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except Exception:
            return {'message': 'Error inserting item'}, 500

        return {'message': 'added item {}, price: {}'.format(item['name'], data['price'])}, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()
        return

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE items SET price=? WHERE name=?', (item['price'], item['name']))
        connection.commit()
        connection.close()

    def delete(self, name):
        row = self.find_by_name(name)
        if row:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute('DELETE FROM items WHERE name=?', (name,))
            return {'message': 'item {} deleted'.format(name)}, 201
        return {'message': 'item {} did not exist'.format(name)}, 404

    def put(self, name):
        row = self.find_by_name(name)

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        if row:
            try:
                self.update(item)
            except:
                return {'message': 'error inserting item'}, 500
        else:
            print('adding')
            try:
                self.insert(item)
            except:
                return {'message': 'error inserting item'}, 500

        return {'message': 'put {}, price {} into db'.format(item['name'], item['price'])}, 201



class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        output = cursor.execute('SELECT * FROM items')
        return {'items': [{'name': row[0], 'price': row[1]} for row in output]}