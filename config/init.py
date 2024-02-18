# importing core Flask modules
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import json
import sys


# this is for getting the secret key
with open('config.json') as f:
    config = json.load(f)

# creating an instance of Flask as our app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SECRET_KEY'] = config['secret_key']
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# creating database connection variable
db = SQLAlchemy()
from .models import User, Item, CartItem, Transaction

db.init_app(app)

# running the site
# creating db if it doesn't exist
if not os.path.exists('instance/store.db'):
    print("Database not found, creating...")
    with app.app_context():
        db.create_all() # Create database tables for our data models

# run this command with any additional arg to run in production
if len(sys.argv) > 1:
    print('<< PROD >>')
    os.system(f"gunicorn -b '0.0.0.0:{config['port']}' app:app")
# or just run without an additional arg to run in debug
else:
    print('<< DEBUG >>')
    app.run(debug=True)

from config import routes
