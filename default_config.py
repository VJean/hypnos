import os

basedir = os.path.abspath(os.path.dirname(__file__))
# sqlalchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# reload on code change
DEBUG = False
# flask-wtforms - csrf
SECRET_KEY = 'secret-key'
# auth
ADMIN_USER = 'admin'
ADMIN_PASSWORD = 'admin'
REMEMBER_COOKIE_DURATION = 30
