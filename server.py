"""server for carbon emmissions app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
import os
from model import connect_to_db
import crud
import requests
from datetime import datetime

app = Flask(__name__)

app_id = os.environ['app_id']
app_key = os.environ['app_key']

from jinja2 import StrictUndefined
#from coolclimate import coolclimate_defaults, existing_user_cc_calcs
#import coolclimate

app.secret_key = "WHATEVERYOUDOTAKECAREOFYOURSHOES"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():

    return render_template("homepage.html")

#TODO: put login handling in own route and redirect to profile once (passwrod and everyhting too) logged in
@app.route('/existing_users')
def existing_user():
    
    import coolclimate #LUCIA ADDED THIS 
    email= request.args.get("email")
    password = request.args.get("password")
    # user_obj = crud.get_user_by_email(email)
    print("THIS IS THE SESSION", session['current_user'])
    # if session.get("current_user"):
    #     user_obj = crud.get_user_by_id(session['current_user'])
    #     print("SESSION CURRENT USER WHAT IS ITTTT", user_obj)
    # else:
    user_obj = crud.get_user_by_email(email)

    if not user_obj:
        flash("Please create account below!")
        return redirect('/')
    elif password:
        if password != user_obj.password:
            print("USER OBJ PASSWORD HERE",user_obj.password)
            print("password in text field:", password)
            flash('incorrect password')

            return redirect('/')
        else:
            session['current_user'] = user_obj.user_id 

    cc_calcs = coolclimate.existing_user_cc_calcs(user_obj.user_id)
    
    elect_bill = cc_calcs['input_footprint_housing_electricity_dollars']
    nat_gas_emit = cc_calcs['input_footprint_housing_naturalgas_dollars']
    vehicle_emit = cc_calcs['input_footprint_transportation_miles1']
    public_trans_emit = cc_calcs['input_footprint_transportation_bus']

    return render_template("profile.html", user_obj=user_obj) #user_obj=user_obj, vehicle_emit=vehicle_emit, 
    #                     nat_gas_emit=nat_gas_emit, public_trans_emit=public_trans_emit, elect_bill=elect_bill) 


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

    return render_template("emission_info.html") #sus

@app.route('/create-new-user')
def create_new_user():

    return render_template("new_user.html")

@app.route('/submit-info', methods=["POST"])
def submit_info():
    
    import coolclimate 

    user_id = session.get('current_user')
    user_obj = crud.get_user_by_id(user_id)
    email = user_obj.email
    location_by_zip = request.form.get("zipcode")
    input_fuel = request.form.get("fuel-type")
    input_mpg = request.form.get("mpg")
    vehicle_travel = request.form.get("vehicle-travel")
    input_public_trans = request.form.get("public-trans")
    input_income = request.form.get("household-income") 
    input_amt = request.form.get("household-amt") 
    input_elect_bill = request.form.get("elect-bill")
    input_nat_gas_bill = request.form.get("nat-gas-bill")
                    
    result = coolclimate.coolclimate_defaults(location_by_zip, input_fuel, input_mpg, vehicle_travel, input_public_trans, input_income, input_amt,
                    input_elect_bill, input_nat_gas_bill)

    location = result["input_location"]
    input_fuel = result["input_footprint_transportation_fuel1"]
    input_mpg = result["input_footprint_transportation_mpg1"]
    vehicle_emit = result["input_footprint_transportation_miles1"]
    public_trans_emit = result["input_footprint_transportation_bus"]
    input_income = result["input_income"]
    input_amt = result["input_size"]
    elect_bill = result["input_footprint_housing_electricity_dollars"]
    nat_gas_emit = result["input_footprint_housing_naturalgas_dollars"]
    
    public_trans_emit = float(public_trans_emit)

    crud.add_mileage(user_id=user_id, mileage=vehicle_travel, carbon_footprint=vehicle_emit, travel_date=datetime.now())

    crud.add_household_info(user_id=user_id, input_amt=input_amt, input_income=input_income, location_by_zip=location)

    crud.add_vehicle_info(input_fuel=input_fuel, input_mpg=input_mpg, user_id=user_id)

    crud.add_public_trans(user_id=user_id, input_public_trans=input_public_trans,carbon_footprint=public_trans_emit)

    crud.add_elect_bill(user_id=user_id, input_elect_bill=input_elect_bill, carbon_footprint=elect_bill)

    crud.add_nat_gas_info(input_nat_gas_bill=input_nat_gas_bill, carbon_footprint=nat_gas_emit, user_id=user_id)

    
    return render_template("profile.html", user_obj=user_obj, vehicle_emit=vehicle_emit, nat_gas_emit=nat_gas_emit, public_trans_emit=public_trans_emit, elect_bill=elect_bill)

@app.route('/user-emission-info.json')
def get_user_emission_info():
    """get the users emission info from the db, store it as json for charts"""

    current_user = session.get('current_user')
    print("CUREENT USER IN SESSION",current_user)
    user_obj = crud.get_user_by_id(current_user)
    monthly_elect = user_obj.monthly_elect[-1].carbon_footprint
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",monthly_elect)
    vehicle_emit = user_obj.vehicle_travel[-1].carbon_footprint
    nat_gas_emit = user_obj.monthly_nat_gas[-1].carbon_footprint
    public_trans_emit = user_obj.public_trans[-1].carbon_footprint

    emission_info = {"labels": ["Electric Emissions", "Vehicle Emissions", "Natural Gass Emissions", "Public Transit Emissions"],
                    "data": [monthly_elect, vehicle_emit, nat_gas_emit, public_trans_emit]
    }
    
    return jsonify(emission_info)

@app.route('/show-update-form')
def show_update_form():

    current_user = session.get('current_user')
    user_obj = crud.get_user_by_id(current_user)

    return render_template("update_info.html")

#TODO: rewrite a funciton that unpacks the result of the API OR 
@app.route('/update-info', methods=["POST"])
def update_info():
    
    import coolclimate

    current_user = session.get('current_user')
    user_obj = crud.get_user_by_id(current_user)
    user_id = session.get('current_user')

    location_by_zip = request.form.get("zipcode")
    input_fuel = request.form.get("fuel-type")
    input_mpg = request.form.get("mpg")
    vehicle_travel = request.form.get("vehicle-travel")
    input_public_trans = request.form.get("public-trans") 
    input_income = user_obj.household[0].income
    input_amt = request.form.get("household-amt") 
    input_elect_bill = request.form.get("elect-bill")
    input_nat_gas_bill = request.form.get("nat-gas-bill")
   
    result = coolclimate.coolclimate_defaults(location_by_zip, input_fuel, input_mpg, vehicle_travel, input_public_trans, input_income, input_amt,
                    input_elect_bill, input_nat_gas_bill)
    
    print("HI IM THER RESULTS", result)
    location = result["input_location"]
    input_fuel = result["input_footprint_transportation_fuel1"]
    input_mpg = result["input_footprint_transportation_mpg1"]
    vehicle_emit = result["input_footprint_transportation_miles1"]
    public_trans_emit = result["input_footprint_transportation_bus"]
    input_income = result["input_income"]
    input_amt = result["input_size"]
    elect_bill = result["input_footprint_housing_electricity_dollars"]
    nat_gas_emit = result["input_footprint_housing_naturalgas_dollars"]
    public_trans_emit = float(public_trans_emit)

    crud.add_mileage(user_id=user_id, mileage=vehicle_travel, carbon_footprint=vehicle_emit)

    crud.add_household_info(user_id=user_id, input_amt=input_amt, input_income=input_income, location_by_zip=location)

    crud.add_vehicle_info(input_fuel=input_fuel, input_mpg=input_mpg, user_id=user_id)

    crud.add_public_trans(user_id=user_id, input_public_trans=input_public_trans,carbon_footprint=public_trans_emit)

    crud.add_elect_bill(user_id=user_id, input_elect_bill=input_elect_bill, carbon_footprint=elect_bill)

    crud.add_nat_gas_info(input_nat_gas_bill=input_nat_gas_bill, carbon_footprint=nat_gas_emit, user_id=user_id)

    
    return render_template('profile.html', user_obj=user_obj)

#TODO: for update info route. It needs to be cleaned up and shorter
 # user_inputs = {'location': request.form.get('zipcode'),
    #                'input_fuel': request.form.get('fuel-type'),
    #               }

    # add_user_info(user_inputs) 
    # >
    # def add_user_info(user_inputs):
    #   result = send_user_inputs_to_api(user_inputs)
    #   add_mileage(user_inputs['user_id'], user_inputs['mileage'], results['input_footprint_transportation_miles1']...)
    #   add_elect_bill(...)
    #   add_nat_gas_bill(...)
    #after you call result son CC defaults
    # def send_user_inputs_to_api(user_inputs):
        # result = coolclimate.coolclimate_defaults(user_inputs['location'], 
        # )
        # return result

if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
   