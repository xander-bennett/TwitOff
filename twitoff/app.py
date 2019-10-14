### TO RUN THIS: FLASK_APP=twitoff flask run ###

# import flask package. flask makes app objects
from flask import Flask, render_template

# create Flask web server, makes the application
def create_app():
    """Create and configure an instance of the flask application."""
    app = Flask(__name__)

# routes determine location
# Routing to home
    @app.route('/')
    def home():
        return render_template('home.html')

    return app
