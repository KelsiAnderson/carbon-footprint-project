"""server for carbon emmissions app."""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "TBD"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():

    return render_template("homepage.html")

#route that takes you to the new use page
@app.route('/new_users', method=['POST'])
def new_user():

    return render_template("new_user.html")
#route that takes you to existing user page


@app.route('/existing_users', method=['POST'])
def existing_user():

    return render_template("existing_user.html")

if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.

    app.run(debug=True, host="0.0.0.0")