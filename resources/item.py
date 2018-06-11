from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel


# every resource has to be a class
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True
    )

    parser.add_argument('store_id',
        type=int,
        required=True
    )

    # override the get method from inheritance
    @jwt_required() # must authenticate before we can call get method
    def get(self, name):
        # # use lambda function for filtering
        # item = filter(lambda x: x['name'] == name, items)
        # # item will be a filter object
        # item = next(item, None)
        # # this will give the first item found by the filter function
        # # None is a default value
        # return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':'An item with name {} already exists'.format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        item.save_to_db()
        return item.json(), 201


    def delete(self, name):
        # global items
        # # overwrite the items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'item deleted'}
        return {'message':'item does not exist'}


    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.price = data['store_id']
        # create or update operated by SQLAlchemy
        item.save_to_db()
        return item.json()


class Items(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
