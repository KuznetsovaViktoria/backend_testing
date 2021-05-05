"""I have created new branch for v4"""

from flask import Flask
from flask_restful import Api
from flask_jwt import *
from security import authenticate, identity
from resources.items import Item, ItemList
from resources.users import UserRegister
from db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)

db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


jwt = JWT(app, authenticate, identity)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<name>')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(debug=True)