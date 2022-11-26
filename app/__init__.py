from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

from .util import dateformat, DateConverter

app = Flask(__name__)
app.jinja_env.filters['dateformat'] = dateformat
app.url_map.converters['date'] = DateConverter

print('Loading default config.')
app.config.from_object('default_config')
try:
    app.config.from_object('config')
    print('Loading custom config file.')
except ImportError:
    print('No custom config found.')

# SQL constraints naming convention
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

# init models database
db = SQLAlchemy(app, metadata=metadata)
# migrations manager
# render_as_batch works arond SQLite's ALTER TABLE limitations
migrate = Migrate(app, db, render_as_batch=True)

# init user management
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

TZ_DB_KEY = app.config['TZ_DB_KEY']


# avoid circular references by calling this import at the end
# (views might reference app)
from app import views
