import sqlite3
con = sqlite3.connect('data.db')
cur = con.cursor()

create_table_users = 'CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY AUTOINCREMENT, username text, password text)'
cur.execute(create_table_users)

create_table_items = 'CREATE TABLE IF NOT EXISTS items(id integer PRIMARY KEY AUTOINCREMENT, name text, price float)'
cur.execute(create_table_items)




con.commit()