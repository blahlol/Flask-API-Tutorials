from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage

class FileStorageField(fields.Field):

    default_error_messages = {
        "invalid": "Not a valid image."
    }

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        
        if not isinstance(value, FileStorage):
            self.fail("invalid")


class ImageSchema(Schema):
    """We will use this schema only for load purpose (i.e) to receive user data
    When the code reaches FileStorageField if will run the _deserialize function"""
    image = FileStorageField(required = True) #this variable name should be same as <input> tag's name attribute. Which is inturn used to access request.files[same_var_name]
