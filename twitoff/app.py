from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user, update_all_users
from .predict import predict_user

def create_app():
    """Create and configure an instance of the Flask Application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['FLASK_ENV'] = config('FLASK_ENV')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('home.html', title='Welcome to Twitoff!', users=User.query.all())
# about page route
    @app.route("/about")
    def preds():
        return render_template('about.html')

# resets the instance, good for development and de-bugging
    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('home.html', title='DB Reset!', users=[])

# This method adds users while also checking to see if they've already been added.
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>/', methods=['GET'])
    def user(name=None, message=''):
        name = (name or request.values['user_name'])
        try:
            if request.method =='POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name,e)
            tweets=[]
            pass
        return render_template('user.html', name=name, tweets=tweets, message=message)

# This decorater routes to the comparison page, and the method compares their tweets
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1 = request.values['user1']
        user2 = request.values['user2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2, tweet_text)
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

# This decorater updates the current crop of tweets for all users, routes to home.html
    @app.route('/update')
    def update():
        update_all_users()
        pass
        return render_template('home.html', users=User.query.all(), title='All Tweets updated!')

    return app
