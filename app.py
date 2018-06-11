'''
Two resources:
item: return information about a single item
items: return a list of all items in the database
'''

from flask import Flask
from flask_restful import Api
# with flask_restful there's no need to use jsonify ()
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, StoreList

app = Flask(__name__)
# this tells SQLALCHEMY that the database lives in the root directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# this turns off flask sqlalchemy tracker to improve some performance
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
app.secret_key = 'top_secret'
api = Api(app)


jwt = JWT(app, authenticate, identity) # /auth endpoint created by JWT


'''
bind all the REST resources here
'''
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/item/<item_name>
api.add_resource(Items, '/items') # http://127.0.0.1/items
api.add_resource(UserRegister, '/register') # http://127.0.0.1/register
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run()
