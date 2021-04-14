from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')


Items = [
    {'name':'chair','price':500},
    {'name':'phone','price':10000},
    {'name':'watch','price':1000}
]
def abort_if_item_doesnt_exist(name):
    if list(filter(lambda x: x['name'] in name, Items)) == []:
        abort(404, message="There's no such item in the shop {}".format(name))
def abort_if_item_already_exists(name):
    if list(filter(lambda x: x['name'] in name, Items)) != []:
        abort(404, message="Item {} is  already exist".format(name))
#item resource
class Item(Resource):
    def get(self, name):
        abort_if_item_doesnt_exist(name)
        get_item = list(filter(lambda x: x['name'] in name, Items))
        return get_item[0]

    def delete(self, name):
        abort_if_item_doesnt_exist(name)
        for i in range(len(Items)):
            if Items[i]['name'] == name:
                l = i
        del Items[l]
        return '', 204

    def post(self, name):
        abort_if_item_already_exists(name)
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True,
        help="Price cannot be blank!")
        args = parser.parse_args()
        print(args)
        item = {
            'name': name, 'price':args['price']
        }
        Items.append(item)
        return item, 201

    def put(self, name):
        if list(filter(lambda x: x['name'] == name, Items)) != []:
            for i in range(len(Items)):
                if Items[i]['name'] == name:
                    l = i
            parser = reqparse.RequestParser()
            parser.add_argument('price', type=float, required=True, help="Price cannot be blank!")
            args = parser.parse_args()
            Items[l]['price'] = args['price']
            return Items[l], 201

        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help="Price cannot be blank!")
        args = parser.parse_args()
        print(args)
        item = {
            'name': name, 'price': args['price']
        }
        Items.append(item)
        return item, 201







api.add_resource(Item, '/items/<name>')


#itemlist resource
class ItemList(Resource):
    def get(self):
        return Items

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('items', type=dict, action='append', help="Name cannot be blank!")
        args = parser.parse_args()
        added = []
        for i in range(len(args['items'])):
            abort_if_item_already_exists(args['items'][i]['name'])
            item = args['items'][i]
            Items.append(item)
            added.append(item)
        return added, 201

api.add_resource(ItemList, '/items')

app.run(debug=True)