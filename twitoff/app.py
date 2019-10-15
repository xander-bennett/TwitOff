"""Main application for twitoff"""
#imports
from flask import Flask, render_template
from .models import DB

def create_app():
    """create and configures an instance of a flask app"""
    app = Flask(__name__)

    # configuring the DB is done before the routes
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('home.html')

    @app.route("/about")
    def preds():
        return render_template('about.html')

    return app
