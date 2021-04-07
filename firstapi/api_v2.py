from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

ITEMS = [
    {'name': 'tshirt',
     'price': 10},
    {
     'name': 'shorts',
     'price': 5
    }
]


def if_shop_exist(name, mes, f):
    print((name in [i['name'] for i in ITEMS]) == f)
    if (name in [i['name'] for i in ITEMS]) == f:
        abort(404, message=mes)


parser_one = reqparse.RequestParser()
parser_one.add_argument('price')

parser_many = reqparse.RequestParser()
parser_many.add_argument('items', type=list, location='json')


class Item(Resource):
    def get(self, name):
        if_shop_exist(name, "Item {} doesn't exist".format(name), False)
        return list(filter(lambda x: x['name'] == name, ITEMS))

    def post(self, name):
        args = parser_one.parse_args()
        if_shop_exist(name, "Item {} already exist".format(name), True)
        ITEMS.append({'name': name, 'price': args['price']})
        return ITEMS[-1], 201

    def delete(self, name):
        if_shop_exist(name, "Item {} doesn't exist".format(name), False)
        del ITEMS[[i['name'] for i in ITEMS].index(name)]
        return '', 204

    def put(self, name):
        args = parser_one.parse_args()
        i = [i['name'] for i in ITEMS]
        if name not in i:
            ITEMS.append({'name': name, 'price': args['price']})
            return ITEMS[-1], 201
        ITEMS[i.index(name)]['price'] = args['price']
        return ITEMS[i.index(name)]['price'], 201


class ItemList(Resource):
    def get(self):
        return ITEMS, 201

    def post(self):
        args = parser_many.parse_args()
        for item in args['items']:
            if_shop_exist(item['name'], "Item {} already exist".format(item['name']), True)
            ITEMS.append({'name': item['name'], 'price': item['price']})
        return ITEMS[len(ITEMS) - len(args['items']):], 201


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<name>')


if __name__ == '__main__':
    app.run(debug=True)