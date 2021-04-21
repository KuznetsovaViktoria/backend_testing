from flask_restful import reqparse, abort, Resource
from flask_jwt import *
from create_db import *


def if_item_exist(name, mes, f):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    row = list(cur.execute('SELECT name FROM items'))
    con.close()
    if ((name, ) in row) == f:
        abort(404, message=mes)


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price')

    @jwt_required()
    def get(self, name):
        if_item_exist(name, "Item {} doesn't exist".format(name), False)
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        item = list(cur.execute('SELECT * FROM items WHERE name=?', (name, )))
        con.close()
        return item, 201

    def post(self, name):
        args = Item.parser.parse_args()
        if_item_exist(name, "Item {} already exist".format(name), True)
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute('INSERT INTO items VALUES (NULL, ?, ?)', (name, args['price'], ))
        for row in cur.execute('SELECT * FROM items WHERE name=?', (name, )):
            print(row)
        con.commit()
        con.close()
        return {'name': name, 'price': args['price']}, 201

    def delete(self, name):
        if_item_exist(name, "Item {} doesn't exist".format(name), False)
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute('DELETE FROM items WHERE name=?', (name, ))
        con.commit()
        con.close()
        return '', 204

    def put(self, name):
        args = Item.parser.parse_args()
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        if (name, ) not in list(cur.execute('SELECT name FROM items')):
            cur.execute('INSERT INTO items VALUES (NULL, ?, ?)', (name, args['price'],))
            return {'name': name, 'price': args['price']}, 201
        cur.execute('UPDATE items SET price=? WHERE name=?', (args['price'], name, ))
        con.commit()
        con.close()
        return args['price'], 201


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items', type=list, location='json')
    # parser.add_argument('items', type=dict, method=append) - можно поменять

    def get(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        items = list(cur.execute('SELECT * FROM items'))
        con.close()
        return items, 201

    def post(self):
        args = ItemList.parser.parse_args()
        a = []
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        row = list(cur.execute('SELECT name FROM items'))
        already_exists = []
        for item in args['items']:
            if (item['name'],) in row:
                already_exists.append(item['name'])
            else:
                a.append((item['name'], item['price'],))
        cur.executemany('INSERT INTO items VALUES (NULL, ?, ?)', a)
        con.commit()
        if already_exists != []:
            abort(404, message=f"Items {', '.join(already_exists)} already exist")
        con.close()
        return a, 201