"""Main application for twitoff"""
#imports
from flask import Flask
from .models import DB

def create_app():
    """create and configures an instance of a flask app"""
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def root():
        return "Welcome to our app"
    return app
