from sqlite3.dbapi2 import Cursor
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request
import sqlite3

items = []

class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        result = cursor.execute('select * from items')
        rows = result.fetchall()
        connection.close()
        
        items = [{'name': row[0], 'price': row[1]} for row in rows]

        return {'items': items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
            'price',
            required = True,
            type = float,
            help = 'This is a required field'
        )

    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return {'item': item}
        return {'message': 'Item not found'}, 404

        # item = next(filter(lambda item: item['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404

    def find_by_name(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        result = cursor.execute('select * from items where name = ?', (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'name': row[0], 'price': row[1]}

    def post(self, name):
        item = self.find_by_name(name)
        
        if item:
            return {'message': 'Item already exists'}, 400

        data = Item.parser.parse_args()

        try:
            self.insert(name, data['price'])
        except:
            return {'message': 'Item insertion failed.'}, 500

        return {'name': name, 'price': data['price']}, 201
    
    @classmethod
    def insert(cls,name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute('insert  into items values (? ,?)', (name, price))
        connection.commit()
        connection.close()
         

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item:
            try:
                self.update(name, data['price']) # update existing item
            except:
                return {'message': 'Item updation failed.'}, 500
        else:
            try:
                self.insert(name, data['price']) # update existing item
            except:
                return {'message': 'Item insertion failed.'}, 500

        return updated_item
    
    @classmethod
    def update(self, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute('update items set price = ? where name = ?', (price, name))
        connection.commit()
        connection.close()
    
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute('delete from items where name = ?', (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted successfully'}
