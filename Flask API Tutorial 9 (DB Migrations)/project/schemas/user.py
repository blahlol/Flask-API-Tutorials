# from marshmallow import Schema, fields

# class UserSchema(Schema):
#     class Meta:
#         load_only = ('password', ) # this tells marshmallow that password should be used only while loading and not dumping
#         dump_only = ('id', )
#     id = fields.Int()
#     username = fields.Str(required = True)
#     password = fields.Str(required = True)

from ma import ma
from models.user import UserModel

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ('password', ) # this tells marshmallow that password should be used only while loading and not dumping
        dump_only = ('id', )
        load_instance = True

