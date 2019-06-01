from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '395eca5d4acf6edb4a709be159d6747f'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from ez import routes