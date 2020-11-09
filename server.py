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

#route that takes you to existing user page
@app.route('/existing_users')
def existing_user():
    
    email= request.args.get("email")
    user_name = request.args.get("username")
    password = request.args.get("password")
    user_by_email = crud.get_user_by_email(email)
    if not user_by_email:
        flash("Please create account below!")
    else:
       #I need to figure out how to prove that the name is already in the database
       #when they sign in, their info successfully logs them into the website
       # and then redirects to existing user
        return render_template("existing_user.html", user_by_email=user_by_email)


@app.route('/new_users', methods=["POST"])
def new_user():
    
    user_name = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    new_user = crud.create_user(user_name, email, password)

    return render_template("emission_info.html")

@app.route('/create-new-user')
def create_new_user():

    return render_template("new_user.html")


if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.

    app.run(debug=True, host="0.0.0.0")