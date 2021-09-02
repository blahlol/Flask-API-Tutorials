from datetime import timedelta
from blocklist import BLOCKLIST
from flask import Flask, jsonify
from flask_restful import Api
from ma import ma
from db import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from marshmallow import ValidationError

from resources.user import UserRegister, User, UserLogin
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:samsungchamp@localhost/dbmigrationtutorial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True #allows the other imported extensions to raise error with suitable error codes. By default it's set to False and raises error with code 500 (internal sevrer error).
app.secret_key = 'somerandomlongstring'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours = 24)
app.config['UPLOADED_IMAGES_DEST'] = os.path.join("static", "images")
api = Api(app)
db.init_app(app)
ma.init_app(app)

@app.errorhandler(ValidationError) #this catches the validation error every time it occurs and it doesnt need to be included as an except block every time we do a load operation. This also needs propogate_exceptions to be set to true
def marshmallow_error(err):
    return jsonify(err.messages)

# @app.before_first_request
# def create_tables():
#     db.create_all()

jwt = JWTManager(app)
migrate = Migrate(app, db)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in BLOCKLIST

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    app.run(port=5000, debug=True)