"""server for carbon emmissions app."""

from flask import (Flask, render_template, request, flash, session, redirect)
import os
from model import connect_to_db
import crud
import requests
from coolclimate import coolclimate_defaults

app = Flask(__name__)

app_id = os.environ['app_id']
app_key = os.environ['app_key']

from jinja2 import StrictUndefined

app.secret_key = "WHATEVERYOUDOTAKECAREOFYOURSHOES"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():

    return render_template("homepage.html")

@app.route('/existing_users')
def existing_user():
    
    email= request.args.get("email")
    user_name = request.args.get("username")
    password = request.args.get("password")
    user_obj = crud.get_user_by_email(email)
    
    if not user_obj:
        flash("Please create account below!")
        return redirect('/')
    else:
        if password != user_obj.password:
            flash('incorrect password')
            return redirect('/')
        else:
            session['current_user'] = user_obj.user_id
        
            current_user = session.get('current_user')
            existing_user_cc_calcs(user_id)

            return render_template("profile.html", user_obj=user_obj, vehicle_emit=vehicle_travel.mileage, 
                                nat_gas_emit=nat_gas_use, public_trans_emit=public_trans, elect_bill=electricity_use) 


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
        session['current_user'] = new_user.user_id
        print("NEW USER", new_user.user_id)

    else:
        flash('User already exists')
        return redirect('/')

    return render_template("emission_info.html")

@app.route('/create-new-user')
def create_new_user():

    return render_template("new_user.html")

@app.route('/submit-info', methods=["POST"])
def submit_info():
    
    user_id = session.get('current_user')
    user_obj = crud.get_user_by_id(user_id)
    email = user_obj.email
    location_by_zip = request.form.get("zipcode")
    input_fuel = request.form.get("fuel-type")
    
    print("LOOK HERE FOR FUEL", input_fuel)
    input_mpg = request.form.get("mpg")
    vehicle_travel = request.form.get("vehicle-travel")
    input_public_trans = request.form.get("public-trans")
    input_income = request.form.get("household-income")
    input_amt = request.form.get("household-amt")
    input_elect_bill = request.form.get("elect-bill")
    input_nat_gas_bill = request.form.get("nat-gas-bill")
    add_all = crud.add_user_info(location_by_zip=location_by_zip, input_fuel=input_fuel, input_mpg=input_mpg, vehicle_travel=vehicle_travel, 
                                input_public_trans=input_public_trans, input_income=input_income, input_amt=input_amt,
                                input_elect_bill=input_elect_bill, input_nat_gas_bill=input_nat_gas_bill, user_id=user_id)

    result = coolclimate_defaults(location_by_zip, input_fuel, input_mpg, vehicle_travel, input_public_trans, input_income, input_amt,
                    input_elect_bill, input_nat_gas_bill)

    for key in result:
        if key == "input_location":
            location = result[key]

        if key == "input_footprint_housing_electricity_dollars":
            elect_bill = result[key]
            
        if key == "input_footprint_transportation_miles1":
            vehicle_emit = result[key]

        if key == "input_footprint_transportation_bus":
            public_trans_emit = result[key]

        if key == "input_footprint_housing_naturalgas_dollars":
            nat_gas_emit = result[key]
        
    return render_template("profile.html", user_obj=user_obj, vehicle_emit=vehicle_emit, nat_gas_emit=nat_gas_emit, public_trans_emit=public_trans_emit, elect_bill=elect_bill)


if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
   