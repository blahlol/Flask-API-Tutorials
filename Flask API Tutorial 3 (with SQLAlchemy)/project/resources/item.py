from flask_restful import Resource, reqparse
from models.item import ItemModel

class Items(Resource):
    def get(self):
        items = ItemModel.query.all()
        items = [item.json() for item in items]

        return {'items': items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
            'price',
            required = True,
            type = float,
            help = 'This is a required field'
        )
    parser.add_argument(
            'store_id',
            required = True,
            type = int,
            help = 'Every item needs a store_id'
        )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

        # item = next(filter(lambda item: item['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        
        if item:
            return {'message': 'Item already exists'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'Item insertion failed.'}, 500

        return item.json(), 201
    
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name = name, price = data['price'], store_id = data['store_id'])
        else:
            item.price = data['price']
        
        item.save_to_db()

        return item.json()
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted successfully'}