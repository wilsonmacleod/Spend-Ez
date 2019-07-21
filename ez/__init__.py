import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'#os.environ.get('EZ_SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = '395eca5d4acf6edb4a709be159d6747f'#os.environ.get('EZ_SECRET_KEY')
    
    db.init_app(app)
    login_manager.init_app(app)

    from ez.main.routes import main
    app.register_blueprint(main)

    return app