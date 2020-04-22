# import the flask package flask makes app objects
from flask import Flask

# create Flask web server, makes the application
app=Flask(__name__)

# routes determine location
@app.route("/")
def hello_world():
    return 'Hello, world!'

@app.route("/about")
def about():
    return 'About page!'