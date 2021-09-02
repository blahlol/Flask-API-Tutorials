from flask_restful import Resource
from flask_uploads import UploadNotAllowed, extension
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, send_file
import os
import traceback

from libs import image_helper

IMAGE_UPLOADED = "Image Uploaded: {}"
INVALID_EXTENSION = "Invalid Extension"
IMAGE_NOT_FOUND = "Image not found."
FILENAME_NOT_SAFE = "Filename is not formatted right."
IMAGE_DELETED = "Image Deleted."
IMAGE_DELETE_FAILED = "Image delete failed."
MISSING_FIELD = "Missing Field: '{}'"

class ImageUpload(Resource):
    @jwt_required()
    def post(self):
        """If there is a filename conflict, it appends a number to the end on its own"""
        data = request.files
        if "image" not in data:
            return {"message": MISSING_FIELD.format('image')}
        user_id = get_jwt_identity()
        folder = f'user_{user_id}'
        try:
            image_path = image_helper.save_image(data['image'], folder = folder)
            basename = image_helper.get_basename(image_path)
            return {"message": IMAGE_UPLOADED.format(basename)}
        except UploadNotAllowed:
            extension = image_helper.get_extension(data['image'])
            return {"message": INVALID_EXTENSION}, 400

class Image(Resource):
    @jwt_required()
    def get(self, filename):
        """Users can get only their images"""
        user_id = get_jwt_identity()
        folder = f'user_{user_id}'

        if not image_helper.is_filename_safe(filename):
            return {"message": FILENAME_NOT_SAFE}, 400

        try:
            return send_file(image_helper.get_path(filename, folder))
        except FileNotFoundError:
            return {"message": IMAGE_NOT_FOUND}, 404
        
    @jwt_required()
    def delete(self, filename):
        user_id = get_jwt_identity()
        folder = f'user_{user_id}'

        if not image_helper.is_filename_safe(filename):
            return {"message": FILENAME_NOT_SAFE}, 400
        
        try:
            os.remove(image_helper.get_path(filename, folder))
            return {"message": IMAGE_DELETED}
        except FileNotFoundError:
            return {"message": IMAGE_NOT_FOUND}, 404
        except:
            traceback.print_exc()
            return {"message": IMAGE_DELETE_FAILED}, 500

class AvatarUpload(Resource):
    @jwt_required()
    def put(self):
        data = request.files
        if "image" not in data:
            return {"message": MISSING_FIELD.format('image')}

        user_id = get_jwt_identity()
        filename = f"user_{user_id}"
        folder = f"avatars"
        avatar_path = image_helper.find_image_any_format(filename, folder)

        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": IMAGE_DELETE_FAILED}

        try:
            extension = image_helper.get_extension(data['image'].filename)
            filename = filename + extension
            avatar_path = image_helper.save_image(data['image'], folder = folder, name = filename)
            basename = image_helper.get_basename(avatar_path)
            return {"message": IMAGE_UPLOADED.format(basename)}
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": INVALID_EXTENSION}

class Avatar(Resource):
    def get(self, user_id):
        folder = "avatars"
        filename = f"user_{user_id}"
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            return send_file(avatar_path)
        return {"message": IMAGE_NOT_FOUND}

