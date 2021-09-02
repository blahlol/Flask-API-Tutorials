from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models.item import ItemModel
from schemas.item import ItemSchema

ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item Deleted."
NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ERROR_INSERTING_ITEM = "An error occurred inserting the item."

item_schema = ItemSchema()
item_list_schema = ItemSchema(many = True)

class Item(Resource):
    @classmethod
    def get(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item)
        return {'message': ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh = True)
    def post(cls, name):
        if ItemModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXISTS.format(name)}, 400

        data = request.get_json() # this does not include name as it is coming from url
        data['name'] = name

        item = item_schema.load(data) # try except not needed as app.errorhandler is set for validationerror in app.py
        # except ValidationError as err:
        #     return err.messages, 400

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING_ITEM}, 500

        return item_schema.dump(item), 201

    @classmethod
    @jwt_required()
    def delete(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': ITEM_DELETED}
        return {'message': ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, name):
        data = request.get_json()
        data['name'] = name

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = item_schema.load(data)

        try:
            item.save_to_db()
        except:
            return {'message': ERROR_INSERTING_ITEM}, 500

        return item_schema.dump(item)


class ItemList(Resource):
    @classmethod
    def get(cls):
        # items =  [item_schema.dump(item) for item in ItemModel.find_all()]
        items = item_list_schema.dump(ItemModel.find_all())
        return {'items': items}
        