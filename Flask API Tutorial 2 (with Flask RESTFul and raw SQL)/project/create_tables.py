import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create = 'create table if not exists users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create)

create = 'create table if not exists items (name text, price real)'
cursor.execute(create)

connection.commit()
connection.close()