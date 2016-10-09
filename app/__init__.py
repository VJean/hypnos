import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# avoid circular references by calling this import at the end
# (views might reference app)
from app import views, models
