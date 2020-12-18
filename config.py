import os
import binascii
from os import path

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """ Config variables of the app """
    # SECRET_KEY for CSRF token
    SECRET_KEY = binascii.hexlify(os.urandom(24))
    # PATH to the database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Icons to import
    FONTAWESOME_STYLES=['all']
    FONTAWESOME_TYPE='svg/js'

    # Upload folder for files
    UPLOAD_FOLDER=path.join('.', 'app', 'static', 'img')