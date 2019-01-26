"""
Flask restful app
"""
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'this_is_georges_secret_key'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

def return_item(name, items):
    return next(filter(lambda x: x['name'] == name, items), None)



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field can\'t be left blank')

    @jwt_required()
    def get(self, name):
        item = return_item(name, items)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if return_item(name, items) is not None:
            return {'message': 'item already exists: {}'.format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return {'message': 'added item {}, price: {}'.format(item['name'], item['price'])}, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item {} deleted'.format(name)}

    def put(self, name):
        data = Item.parser.parse_args()

        item = return_item(name, items)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
