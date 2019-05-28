from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '395eca5d4acf6edb4a709be159d6747f'
db = SQLAlchemy(app)

from ez import routes