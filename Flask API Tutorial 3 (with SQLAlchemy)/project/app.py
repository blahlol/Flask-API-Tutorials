from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.secret_key = 'somesecretkeyforjwt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
api = Api(app)
jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/test')
@jwt_required()
def test():
    return f'{current_identity}'

api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug = True)