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
    """show homepage"""

    return render_template("homepage.html")

#TODO: put login handling in own route and redirect to profile once (passwrod and everyhting too) logged in
@app.route('/existing_users')
def existing_user():
    """determine if the user logging in already has a profile or not. If they do, check if the 
        password is valid. If the password is not valid flash a message. 
        If it is, log them in and show their profile page with emission info."""

    import coolclimate 
    email= request.args.get("email")
    password = request.args.get("password")
    
    user_obj = crud.get_user_by_email(email)

    if not user_obj:
        flash("Please create account below!")
        return redirect('/')
    elif password:
        if password != user_obj.password:
            flash('incorrect password')

            return redirect('/')
        else:
            session['current_user'] = user_obj.user_id 

    cc_calcs = coolclimate.existing_user_cc_calcs(user_obj.user_id)
    
    elect_emit = cc_calcs['input_footprint_housing_electricity_dollars']
    nat_gas_emit = cc_calcs['input_footprint_housing_naturalgas_dollars']
    vehicle_emit = cc_calcs['input_footprint_transportation_miles1']
    public_trans_emit = cc_calcs['input_footprint_transportation_bus']

    crud.change_vehicle_carbon(user_obj.user_id, vehicle_emit)
    crud.change_gas_carbon(user_obj.user_id, nat_gas_emit)
    crud.change_elect_carbon(user_obj.user_id, elect_emit)
    crud.change_public_trans_carbon(user_obj.user_id, public_trans_emit)

    month = datetime.now().month
    year = datetime.now().year
    date = datetime.now()
    last_month = month - 1
    current_elect_emission = crud.compare_monthly_elect(user_obj.user_id, month, year)
    previous_elect_emission = crud.compare_monthly_elect(user_obj.user_id, last_month, year)
    
    current_nat_gas_emit= crud.compare_monthly_nat_gas(user_obj.user_id, month, year)
    previous_month_gas_emit = crud.compare_monthly_nat_gas(user_obj.user_id, last_month, year)
    
    current_vehicle_emit = crud.compare_monthly_vehicle_emissions(user_obj.user_id, month, year)
    previous_month_vehicle_emit = crud.compare_monthly_vehicle_emissions(user_obj.user_id, last_month, year)
    
    current_public_trans_emit = crud.compare_monthly_public_trans(user_obj.user_id, month, year)
    previous_month_public_trans_emit = crud.compare_monthly_public_trans(user_obj.user_id, last_month, year)

    if previous_month_gas_emit or previous_month_vehicle_emit or previous_month_public_trans_emit:
        show_previous_month = True
    else:
        show_previous_month = False


    
    return render_template("profile.html", user_obj=user_obj, vehicle_emit=vehicle_emit, 
                        nat_gas_emit=nat_gas_emit, public_trans_emit=public_trans_emit, elect_emit=elect_emit, 
                        current_elect_emission=current_elect_emission, 
                        previous_elect_emission=previous_elect_emission, current_nat_gas_emit=current_nat_gas_emit,
                        previous_month_gas_emit=previous_month_gas_emit,
                        current_vehicle_emit=current_vehicle_emit,  previous_month_vehicle_emit= previous_month_vehicle_emit, 
                        current_public_trans_emit=current_public_trans_emit, 
                        previous_month_public_trans_emit=previous_month_public_trans_emit, 
                        show_previous_month=show_previous_month,
                        show_current_month = True
) 

@app.route("/show-profile-page")
def show_profile_page():


    month = datetime.now().month
    year = datetime.now().year
    last_month = month - 1 # (20 + 14 days) % 31 --> Jan 3rd ( 34 % 31 = 3 )
    user = session.get('current_user') # user id
    user_obj = crud.get_user_by_id(user)
    current_elect_emission = crud.compare_monthly_elect(user, month, year)
    previous_elect_emission = crud.compare_monthly_elect(user, last_month, year)

    current_nat_gas_emit= crud.compare_monthly_nat_gas(user, month, year)
    previous_month_gas_emit = crud.compare_monthly_nat_gas(user, last_month, year)
    
    current_vehicle_emit = crud.compare_monthly_vehicle_emissions(user, month, year)
    previous_month_vehicle_emit = crud.compare_monthly_vehicle_emissions(user, last_month, year)
    
    current_public_trans_emit = crud.compare_monthly_public_trans(user, month, year)
    previous_month_public_trans_emit = crud.compare_monthly_public_trans(user, last_month, year)

    if previous_month_gas_emit or previous_month_vehicle_emit or previous_month_public_trans_emit:
        show_previous_month = True
    else:
        show_previous_month = False

    return render_template("profile.html", user_obj=user_obj, 
                        current_elect_emission=current_elect_emission, 
                        previous_elect_emission=previous_elect_emission, current_nat_gas_emit=current_nat_gas_emit,
                        previous_month_gas_emit=previous_month_gas_emit,
                        current_vehicle_emit=current_vehicle_emit,  previous_month_vehicle_emit= previous_month_vehicle_emit, 
                        current_public_trans_emit=current_public_trans_emit, 
                        previous_month_public_trans_emit=previous_month_public_trans_emit, 
                        show_previous_month=show_previous_month,
                        show_current_month = True)

@app.route('/new_users', methods=["POST","GET"])
def new_user():
    """Show a form for new users to create an account. 
        If they are already a user, it will redirect to login page."""
    
    email= request.form.get("new-user-email")
    user_by_email = crud.get_user_by_email(email)
    print("THIS IS EMIAL", user_by_email)
    if not user_by_email:
        fname = request.form.get("new-user-f-name")
        user_name = request.form.get("new-user-username")
        email = request.form.get("new-user-email")
        password = request.form.get("new-user-password")
        new_user = crud.create_user(fname, user_name, email, password)
        session['current_user'] = new_user.user_id
        print("NEW USER", new_user.user_id)

    else:
        flash('User already exists')
        return redirect('/')

    return render_template("emission_info.html")

@app.route('/create-new-user')
def create_new_user():
    """Show the new user form page."""

    return render_template("new_user.html")

@app.route('/submit-info', methods=["POST"])
def submit_info():
    """Show a page that allows a new user to fill out their travel, 
        electric, and natrual gas usage."""

    import coolclimate 

    user_id = session.get('current_user')
    user_obj = crud.get_user_by_id(user_id)
    #email = user_obj.email
    location_by_zip = request.form.get("zipcode")
    input_fuel = request.form.get("fuel-type")
    input_mpg = request.form.get("mpg")
    vehicle_travel = request.form.get("vehicle-travel")
    input_public_trans = request.form.get("public-trans")
    input_income = request.form.get("household-income") 
    input_amt = request.form.get("household-amt") 
    input_elect_bill = request.form.get("elect-bill")
    input_nat_gas_bill = request.form.get("nat-gas-bill")

    
                    
    result = coolclimate.coolclimate_defaults(location_by_zip, 
        input_fuel, input_mpg, vehicle_travel, input_public_trans, 
        input_income, input_amt, input_elect_bill, input_nat_gas_bill)

    location = result["input_location"]
    input_fuel = result["input_footprint_transportation_fuel1"]
    input_mpg = result["input_footprint_transportation_mpg1"]
    vehicle_emit = result["input_footprint_transportation_miles1"]
    public_trans_emit = result["input_footprint_transportation_bus"]
    input_income = result["input_income"]
    input_amt = result["input_size"]
    elect_emit = result["input_footprint_housing_electricity_dollars"]
    nat_gas_emit = result["input_footprint_housing_naturalgas_dollars"]
    
    public_trans_emit = float(public_trans_emit)


    crud.add_mileage(user_id=user_id, mileage=vehicle_travel, carbon_footprint=vehicle_emit, travel_date=datetime.now())
    crud.add_household_info(user_id=user_id, input_amt=input_amt, input_income=input_income, location_by_zip=location)
    crud.add_vehicle_info(input_fuel=input_fuel, input_mpg=input_mpg, user_id=user_id)
    crud.add_public_trans(user_id=user_id, input_public_trans=input_public_trans,carbon_footprint=public_trans_emit)
    crud.add_elect_bill(user_id=user_id, input_elect_bill=input_elect_bill, carbon_footprint=elect_emit)
    crud.add_nat_gas_info(input_nat_gas_bill=input_nat_gas_bill, carbon_footprint=nat_gas_emit, user_id=user_id)

    month = datetime.now().month
    year = datetime.now().year
    last_month = month - 1

    current_elect_emission = crud.compare_monthly_elect(user_obj.user_id, month, year)
    previous_elect_emission = crud.compare_monthly_elect(user_obj.user_id, last_month, year)
    
    current_nat_gas_emit= crud.compare_monthly_nat_gas(user_obj.user_id, month, year)
    previous_month_gas_emit = crud.compare_monthly_nat_gas(user_obj.user_id, last_month, year)
    
    current_vehicle_emit = crud.compare_monthly_vehicle_emissions(user_obj.user_id, month, year)
    previous_month_vehicle_emit = crud.compare_monthly_vehicle_emissions(user_obj.user_id, last_month, year)
    
    current_public_trans_emit = crud.compare_monthly_public_trans(user_obj.user_id, month, year)
    previous_month_public_trans_emit = crud.compare_monthly_public_trans(user_obj.user_id, last_month, year)

    return render_template("profile.html", user_obj=user_obj, 
        current_elect_emission=current_elect_emission, 
        previous_elect_emission=previous_elect_emission, 
        current_nat_gas_emit=current_nat_gas_emit, 
        previous_month_gas_emit=previous_month_gas_emit,
        current_vehicle_emit=current_vehicle_emit, 
        previous_month_vehicle_emit=previous_month_vehicle_emit, 
        current_public_trans_emit=current_public_trans_emit, 
        previous_month_public_trans_emit=previous_month_public_trans_emit, 
        show_previous_month = False,
        show_current_month = True

    )


@app.route('/show-update-form')
def show_update_form():
    """Show page to update existing users tavel, electric, and gas usage"""

    current_user = session.get('current_user')
    user_obj = crud.get_user_by_id(current_user)

    return render_template("update_info.html")

#TODO: rewrite a funciton that unpacks the result of the API OR 
@app.route('/update-info', methods=["POST"])
def update_info():
    """Grab the info that the user updates in the form, send it to the API, 
        grab the results from the API, and show it on the profile page."""
    
    import coolclimate

    current_user = session.get('current_user')
    user_obj = crud.get_user_by_id(current_user)
    user_id = session.get('current_user')

    month = datetime.now().month
    year = datetime.now().year
    date = datetime.now()
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
    elect_emit = result["input_footprint_housing_electricity_dollars"]
    nat_gas_emit = result["input_footprint_housing_naturalgas_dollars"]
    public_trans_emit = float(public_trans_emit)

    crud.add_mileage(user_id=user_id, mileage=vehicle_travel, carbon_footprint=vehicle_emit)
    crud.add_household_info(user_id=user_id, input_amt=input_amt, input_income=input_income, location_by_zip=location)
    crud.add_vehicle_info(input_fuel=input_fuel, input_mpg=input_mpg, user_id=user_id)
    crud.add_public_trans(user_id=user_id, input_public_trans=input_public_trans,carbon_footprint=public_trans_emit)
    crud.add_elect_bill(user_id=user_id, input_elect_bill=input_elect_bill, carbon_footprint=elect_emit)
    crud.add_nat_gas_info(input_nat_gas_bill=input_nat_gas_bill, carbon_footprint=nat_gas_emit, user_id=user_id)


    month = datetime.now().month
    year = datetime.now().year
    date = datetime.now()
    last_month = month - 1
    current_elect_emission = crud.compare_monthly_elect(user_obj.user_id, month, year)
    previous_elect_emission = crud.compare_monthly_elect(user_obj.user_id, last_month, year)
    
    current_nat_gas_emit= crud.compare_monthly_nat_gas(user_obj.user_id, month, year)
    previous_month_gas_emit = crud.compare_monthly_nat_gas(user_obj.user_id, last_month, year)
    
    current_vehicle_emit = crud.compare_monthly_vehicle_emissions(user_obj.user_id, month, year)
    previous_month_vehicle_emit = crud.compare_monthly_vehicle_emissions(user_obj.user_id, last_month, year)
    
    current_public_trans_emit = crud.compare_monthly_public_trans(user_obj.user_id, month, year)
    previous_month_public_trans_emit = crud.compare_monthly_public_trans(user_obj.user_id, last_month, year)

    return render_template('profile.html', user_obj=user_obj,
        current_elect_emission=current_elect_emission, 
        previous_elect_emission=previous_elect_emission, 
        current_nat_gas_emit=current_nat_gas_emit,
        previous_month_gas_emit=previous_month_gas_emit,
        current_vehicle_emit=current_vehicle_emit,  
        previous_month_vehicle_emit= previous_month_vehicle_emit, 
        current_public_trans_emit="{:.2f}".format(current_public_trans_emit), 
        previous_month_public_trans_emit=previous_month_public_trans_emit,
        show_previous_month= True, 
        show_current_month = True
    )


@app.route('/user-emission-info.json')
def get_user_emission_info():
    """get the users current month emission info from the db, 
        store it as json for current month charts"""

    current_user = session.get('current_user')
    user_obj = crud.get_user_by_id(current_user)
    month = datetime.now().month
    year = datetime.now().year
    #date = datetime.now()
    #last_month = month - 1
 #TODO: 
 #updated values if they arte zero
    monthly_elect = crud.compare_monthly_elect(user_obj.user_id, month, year)
    vehicle_emit = crud.compare_monthly_vehicle_emissions(user_obj.user_id, month, year)
    nat_gas_emit = crud.compare_monthly_nat_gas(user_obj.user_id, month, year)
    public_trans_emit = crud.compare_monthly_public_trans(user_obj.user_id, month, year)

    print("SEE PUBLIC TRANSIT ****************", public_trans_emit)
    print("MONTHLY ELECTRICITY HERE #######################", monthly_elect)

    emission_info = {"labels": ["Electricity Emissions", "Vehicle Emissions", "Natural Gas Emissions", "Public Transit Emissions"],
                    "data": [monthly_elect, vehicle_emit, nat_gas_emit, "{:.2f}".format(public_trans_emit)]
    }
    print("EMISSION INFO*******", emission_info)
    return jsonify(emission_info)


@app.route('/previous-month-user-emission-info.json')
def previous_month_user_emission_info():
    """Get the users previous month emission info from the db, 
        store it as json for previous month charts."""

    current_user = session.get('current_user')
    user_obj = crud.get_user_by_id(current_user)
    month = datetime.now().month
    year = datetime.now().year
    last_month = month - 1
    
    previous_elect_emission = crud.compare_monthly_elect(user_obj.user_id, last_month, year)
    #print("SEEE PREVIOS ELECT EMISSSS ------------", previous_elect_emission)
    previous_month_gas_emit = crud.compare_monthly_nat_gas(user_obj.user_id, last_month, year)
    previous_month_vehicle_emit = crud.compare_monthly_vehicle_emissions(user_obj.user_id, last_month, year)
    previous_month_public_trans_emit = crud.compare_monthly_public_trans(user_obj.user_id, last_month, year)

    previous_month_emit_info = {"labels": ["Electricity Emissions", "Vehicle Emissions", "Natural Gas Emissions", "Transit Emissions"],
                                "data": [previous_elect_emission, previous_month_vehicle_emit, previous_month_gas_emit, previous_month_public_trans_emit]}

    return jsonify(previous_month_emit_info)

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
   