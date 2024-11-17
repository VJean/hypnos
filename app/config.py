import os
from datetime import timedelta

# sqlalchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ["HYPNOS_DB_PATH"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
# reload on code change
DEBUG = False
# flask-wtforms - csrf
SECRET_KEY = os.environ.get("HYPNOS_CSRF_SECRET_KEY")
# TimezoneDB API Key
TZ_DB_KEY = os.environ.get("HYPNOS_TZ_DB_KEY")
# auth
ADMIN_USER = os.environ.get("HYPNOS_ADMIN_USER")
ADMIN_PASSWORD = os.environ.get("HYPNOS_ADMIN_PASS")
REMEMBER_COOKIE_DURATION = timedelta(days=30)
