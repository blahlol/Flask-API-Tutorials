import os
import re
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES) #all images will now be saved under static/images

def save_image(image, folder = None, name = None):
    return IMAGE_SET.save(image, folder, name)

def get_path(filename = None, folder = None):
    return IMAGE_SET.path(filename, folder)

def find_image_any_format(filename, folder):
    for format in IMAGES:
        image = f'{filename}.{format}'
        image_path = IMAGE_SET.path(image, folder)
        if os.path.isfile(image_path):
            return image_path
    return None

def retrieve_filename(file): 
    """
    here file could be a str or a FileStorage object.
    If it is a string then we return it as such because it is already the name that we are looking for.
    If it is a FileStorage object then we return file.filename where, file in this case is the FileStorage object.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file

def is_filename_safe(file):
    filename = retrieve_filename(file)
    allowed_formats = "|".join(IMAGES) #allowed_formats = "jpeg|jpg|png|svg" and so on. This includes all the formats mentioned in IMAGES

    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_formats})$"
    return re.match(regex, filename)

def get_basename(file):
    filename = retrieve_filename(file)
    return os.path.split(filename)[1]

def get_extension(file):
    filename = retrieve_filename(file)
    return os.path.splitext(filename)[1]