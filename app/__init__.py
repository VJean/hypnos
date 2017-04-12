from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# try to load conf
try:
    app.config.from_object('config')
    print('Loading custom config file.')
except ImportError:
    app.config.from_object('default_config')
    print('No custom config found, loading default file.')

# init models database
db = SQLAlchemy(app)
# init user management
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)


# avoid circular references by calling this import at the end
# (views might reference app)
from app import views
