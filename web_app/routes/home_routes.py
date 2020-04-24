from flask import Blueprint

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def hello_world():
    print("YOU VISITED THE HOMEPAGE")
    return "Hello, World!"

@home_routes.route("/about")
def about():
    print("YOU VISITED THE ABOUT PAGE")
    return "About Me (TODO)"