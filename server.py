"""server for carbon emmissions app."""

from flask import (Flask, render_template, request, flash, session, redirect)
import os
from model import connect_to_db
import crud
import requests

app = Flask(__name__)

app_id = os.environ['app_id']
app_key = os.environ['app_key']

from jinja2 import StrictUndefined

app.secret_key = "WHATEVERYOUDOTAKECAREOFYOURSHOES"
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
        return redirect('/')
    else:
        if password != user_by_email.password:
            flash('incorrect password')
            return redirect('/')
        else:
            session['current_user'] = user_by_email.user_id
        
            current_user = session.get('current_user')
            vehicle_travel = crud.get_vehicle_travel_by_user(current_user)
            electricity_use = crud.get_monthly_elect_by_user(current_user)
            nat_gas_use = crud.get_monthly_nat_gas_by_user(current_user)

            return render_template("existing_user.html", user_by_email=user_by_email, vehicle_travel=vehicle_travel, electricity_use=electricity_use, nat_gas_use=nat_gas_use)


@app.route('/new_users', methods=["POST","GET"])
def new_user():
    
    email= request.form.get("email")
    user_by_email = crud.get_user_by_email(email)
    print(user_by_email)
    if not user_by_email:
        fname = request.form.get("fname")
        user_name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        new_user = crud.create_user(fname, user_name, email, password)
    else:
        print('LOOOKKK ATTT MEEEE')
        flash('User already exists')
        return redirect('/')

    return render_template("emission_info.html")

@app.route('/create-new-user')
def create_new_user():

    return render_template("new_user.html")

@app.route('/get-emission-info')
def get_emission_info():
    
    flash("You are now logged in")
    return render_template("emission_info.html")


@app.route('/get-emission-info', methods=['POST'])
def receive_emission_info():

    input_fuel = request.form.get("fuel-type")
    print("FUEL HEREEE", input_fuel)
    input_mpg = request.form.get("mpg")
    vehicle_travel = request.form.get("vehicle-travel")
    input_public_trans = request.form.get("public-trans")
    input_income = request.form.get("household-income")
    input_amt = request.form.get("household-amt")
    input_elect_bill = request.form.get("elect-bill")
    input_nat_gas_bill = request.form.get("nat-gas-bill")

    coolclimate_defaults(input_fuel, input_mpg, input_public_trans, 
                input_income, input_amt, input_elect_bill, input_nat_gas_bill)

    return render_template("existing_user.html", input_fuel=input_fuel, input_mpg=input_mpg, vehicle_travel=vehicle_travel,
    input_public_trans=input_public_trans, input_income=input_income, input_amt=input_amt, 
    input_elect_bill=input_elect_bill, input_nat_gas_bill=input_nat_gas_bill)


def coolclimate_defaults(input_fuel, input_mpg, vehicle_travel, input_public_trans, 
                    input_income, input_amt, input_elect_bill, 
                    input_nat_gas_bill):
    #add header and refer to variables app_id and app_key not actual keys
    #params/payload
    #request.get from below
    #connect user response
    url = "https://apis.berkeley.edu/coolclimate/footprint-sandbox"
    payload = {'input_income': input_income, 
            'input_footprint_transportation_miles1': vehicle_travel, 
            'input_footprint_transportation_fuel1': 1, 
            'input_footprint_transportation_mpg1': 32, 
            'input_size': 1}
    
    headers = (app_id, app_key)
    
    response = requests.get("https://apis.berkeley.edu/coolclimate/footprint-sandbox", params=payload, headers=headers)

    data = response.json()
    print(data)
    # income = data['_embedded']['input_income']
    return data


if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
   