from flask import Flask

def create_app():
    """Create and configure an instance of the flask application."""
    app = Flask(__name__)

    @app.route('/')
    def root():
        return 'Hello TwitOff!!'

    return app

