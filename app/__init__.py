from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

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

# init models database
db = SQLAlchemy(app)
# init user management
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)


# avoid circular references by calling this import at the end
# (views might reference app)
from app import views
