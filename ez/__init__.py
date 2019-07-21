import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('EZ_SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.environ.get('EZ_SECRET_KEY')
    
    db.init_app(app)
    login_manager.init_app(app)

    from ez.main.routes import main
    app.register_blueprint(main)

    return app