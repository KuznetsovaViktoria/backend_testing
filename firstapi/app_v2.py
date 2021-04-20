from flask import Flask
from flask_restful import Api
from flask_jwt import *
from security import authenticate, identity
from items import Item, ItemList
from Users import UserRegister

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret' # формальность, которой мы не пользуемся
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<name>')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(debug=True)