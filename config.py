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
    SQLALCHEMY_DATABASE_URI = 'postgres://pwwgkcaaevafbv:5ead1012ac5933ad93a32e122e7d1a7b538a225095a592cfe87c6e0af4213c1d@ec2-44-197-40-76.compute-1.amazonaws.com:5432/d1cnfs6q3001su'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    #     'sqlite:///' + os.path.join(basedir, 'image.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
