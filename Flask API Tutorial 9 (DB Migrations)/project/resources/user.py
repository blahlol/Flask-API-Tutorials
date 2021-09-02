from blocklist import BLOCKLIST
from flask import request
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from models.user import UserModel
from schemas.user import UserSchema
from marshmallow import ValidationError

USER_ALREADY_EXISTS = "A user with that username already exists"
USER_CREATED = "User created successfully."
USER_DOES_NOT_EXIST = 'User does not exist.'
USER_DELETED = 'User deleted.'
INVALID_CREDENTIALS = 'Invalid Credentials'
USER_LOGGED_OUT = 'User Logged out'
BLANK_ERROR = "This field cannot be left blank!"

user_schema = UserSchema()

class UserRegister(Resource):
    @classmethod
    def post(cls):

        user = user_schema.load(request.get_json()) # this gives user obj instead of a dict like in case of vanilla marshmallow

        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400
        
        user.save_to_db()

        return {"message": USER_CREATED}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
             return user_schema.dump(user)
        return {'message': USER_DOES_NOT_EXIST}, 404

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'message': USER_DELETED}, 200
        return {'message': USER_DOES_NOT_EXIST}, 404


class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        user_from_db = UserModel.find_by_username(user.username)
        if user_from_db and safe_str_cmp(user_from_db.password, user.password):
            access_token = create_access_token(identity = user_from_db.id, fresh = True)
            refresh_token = create_refresh_token(user_from_db.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}

        return {'message': INVALID_CREDENTIALS}, 401