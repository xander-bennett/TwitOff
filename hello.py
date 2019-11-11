# import the flask package flask makes app objects
from flask import Flask

# create Flask web server, makes the application
app=Flask(__name__)

# routes determine location
@app.route("/")

# #define simple function
# def home():
#     return render_template('home.html')
