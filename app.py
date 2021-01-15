# for pylance import issues follow below link
# https://github.com/microsoft/pylance-release/blob/main/TROUBLESHOOTING.md#unresolved-import-warnings

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import identity, authenticate
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'vikas'
api = Api(app)


# create tables in your DB before first request hits your app.
# It looks at import statements at top and create table where ever needed.
# If you forget to import any file which has table definitiion then that
# table will not be created


jwt = JWT(app, authenticate, identity)  # this creates /auth endpoint


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)
