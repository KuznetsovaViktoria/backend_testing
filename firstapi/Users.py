import sqlite3
from flask_restful import reqparse, Resource, abort
from create_db import *


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @staticmethod
    def find_by_username(username):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = 'SELECT * FROM users WHERE username=?'
        row = cur.execute(query, (username, )).fetchone()

        con.close()

        user = User(*row) if row else None
        return user

    @staticmethod
    def find_by_id(_id):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        row = cur.execute(query, (_id, )).fetchone()

        con.close()

        user = User(*row) if row else None
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)

    create_user = 'INSERT INTO users VALUES (NULL, ?, ?)'
    user_existance = 'SELECT * FROM users WHERE username=?'

    def post(self):
        args = UserRegister.parser.parse_args()
        username = args['username']
        password = args['password']
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        row = cur.execute(UserRegister.user_existance, (username, )).fetchone()
        if row:
            abort(404, message=f"User {username} already exists")
        cur.execute(UserRegister.create_user, (username, password, ))
        con.commit()
        return args