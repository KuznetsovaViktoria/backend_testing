from flask_restful import reqparse, abort, Resource
from flask_jwt import *
from models.items import Item as ItemModel


def if_item_exist(name, mes, f):
    if (ItemModel.get(name) != None) == f:
        abort(404, message=mes)


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price')

    @jwt_required()
    def get(self, name):
        if_item_exist(name, "Item {} doesn't exist".format(name), False)
        item = ItemModel.get(name)
        item.jsoning()
        return item.json, 201

    def post(self, name):
        args = Item.parser.parse_args()
        if_item_exist(name, "Item {} already exist".format(name), True)
        ItemModel.post(name, args['price'])
        return {'name': name, 'price': args['price']}, 201

    def delete(self, name):
        if_item_exist(name, "Item {} doesn't exist".format(name), False)
        ItemModel.delete(name)
        return '', 204

    def put(self, name):
        args = Item.parser.parse_args()
        if not ItemModel.get(name):
            ItemModel.post(name, args['price'])
            return {'name': name, 'price': args['price']}, 201
        item = ItemModel.get(name)
        item.price = args['price']
        return args['price'], 201


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items', type=list, location='json')

    def get(self):
        i = ItemModel.get_all()
        items = []
        for item in i:
            item.jsoning()
            items.append(item.json)
        return items, 201

    def post(self):
        args = ItemList.parser.parse_args()
        a = []
        already_exists = []
        for item in args['items']:
            if ItemModel.get(item['name']):
                already_exists.append(item['name'])
            else:
                a.append({'name': item['name'], 'price': item['price']})
                ItemModel.post(item['name'], item['price'])
        if already_exists:
            abort(404, message=f"Items {', '.join(already_exists)} already exist")
        return a, 201