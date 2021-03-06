from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity
from user import UserRegister
from item import Item, Items

app = Flask(__name__)
app.secret_key = 'somesecretkeyforjwt'
api = Api(app)
jwt = JWT(app, authenticate, identity)

@app.route('/test')
@jwt_required()
def test():
    return f'{current_identity}'

api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug = True)