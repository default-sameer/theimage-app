import os 
basedir = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'app/static/uploads')

class Config(object):
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
    SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    #     'sqlite:///' + os.path.join(basedir, 'image.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
