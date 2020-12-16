import os
from tempfile import mkdtemp
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

#Silence warnings
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configure session to use filesystem (instead of signed cookies)
SESSION_FILE_DIR = mkdtemp()
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"

# DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://postgres:secret@127.0.0.1:5432/fyyur'
