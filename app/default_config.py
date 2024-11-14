import os
import pathlib
from datetime import timedelta

basedir = pathlib.PurePath(os.path.abspath(os.path.dirname(__file__))).parent
# sqlalchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
# reload on code change
DEBUG = False
# flask-wtforms - csrf
SECRET_KEY = 'secret-key'
# TimezoneDB API Key
TZ_DB_KEY = ''
# auth
ADMIN_USER = 'admin'
ADMIN_PASSWORD = 'admin'
REMEMBER_COOKIE_DURATION = timedelta(days=30)
