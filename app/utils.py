"""The files defines several useful functions and decorators."""

from re import sub
from werkzeug.datastructures import FileStorage
import os
from config import Config


def save_picture(picture: FileStorage, type: str, id: int) -> str:
    """Saves a picture to the static directory

    Args:
        picture (FileStorage): the picture to save
        type (str): 'profile' or 'recipe'
        id (int): Id of the profile/recipe

    Raises:
        ValueError: if the file type is not supported

    Returns:
        str: URL of the image
    """
    # Find sub url
    if type == 'profile':
        sub_url = 'profiles'
    else:
        sub_url = 'recipes'

    print(picture)

    # Get type of file
    file_type = picture.content_type
    if file_type == 'image/png':
        file_ext = '.png'
    elif file_type in ('image/jpg', 'image/jpeg'):
        file_ext = '.jpg'
    else:
        raise ValueError('Type de fichier non supporté : \'%s\'' % file_type)

    # Create file name
    file_name = '%d%s' % (id, file_ext)

    # Create directory if it doesn't exist
    directory = os.path.join(Config.UPLOAD_FOLDER, sub_url)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Remove previous versions
    jpg_path = os.path.join(directory, '%d.jpg' % id)
    if os.path.exists(jpg_path):
        os.remove(jpg_path)
    png_path = os.path.join(directory, '%d.png' % id)
    if os.path.exists(png_path):
        os.remove(png_path)

    # Save picture
    picture.save(os.path.join(directory, file_name))

    # return url of file
    return '/static/img/%s/%s' % (sub_url, file_name)