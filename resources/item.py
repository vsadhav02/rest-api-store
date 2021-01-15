from flask_restful import Resource,  reqparse
from flask_jwt import jwt_required
import sqlite3

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    # this decorator asks app to authenticate first before calling this endpoint

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}

    def post(self, name):
        # before trying to create new request check if item already exists
        if ItemModel.find_by_name(name):
            return {'message': "An entry matching '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            # Internal server error code
            return {'message': 'Internal error accored while inserting data'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted!!"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            # if item found update price
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']  # if item not found create new item
            item.store_id = data['store_id']

        # This step can do insert or update as well.
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
