"""Main application for twitoff"""
#imports
from decouple import config
from flask import Flask, render_template, request
from .models import DB, User

def create_app():
    """create and configures an instance of a flask app"""
    app = Flask(__name__)

    # configuring the DB is done before the routes
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('ENV') # should change this later to production
    app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False


    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset', users=[])

    @app.route("/about")
    def preds():
        return render_template('about.html')

    # @app.route('/user', methods=['POST'])
    # @app.route('/user/<name>/', methods=['GET'])
    # def user(name=None):
    #     name = name or request.values['user_name']
    #     tweets = User.query.filter(User.name == name).one().tweets
    #     return render_template('user.html', name=name, tweets=tweets)

    return app
