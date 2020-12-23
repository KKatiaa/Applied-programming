from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'dev'
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://' + app.config['DBUSER'] + ':' + app.config['DBPASS'] + '@' \
               + app.config['DBHOST'] + '/' + app.config['DBNAME']

SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

from app import views
