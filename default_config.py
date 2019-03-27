import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
# sqlalchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
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
