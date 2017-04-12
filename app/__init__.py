import os
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# try to load conf
basedir = os.path.abspath(os.path.dirname(__file__))
if os.path.isfile(os.path.join(basedir, "config.py")):
    print('Loading custom config file.')
    app.config.from_object('config')
else:
    print('No custom config found, loading default file.')
    app.config.from_object('default_config')

# init models database
db = SQLAlchemy(app)
# init user management
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)


# avoid circular references by calling this import at the end
# (views might reference app)
from app import views
