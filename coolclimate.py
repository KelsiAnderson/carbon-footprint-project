
import os
import requests
from model import User, connect_to_db, db
import crud

app_id = os.environ['app_id']
app_key = os.environ['app_key']

def coolclimate_defaults(location_by_zip, input_fuel, input_mpg, vehicle_travel, input_public_trans, input_income, input_amt,
                    input_elect_bill, input_nat_gas_bill):

    payload = {"input_location_mode": 1, 
            "input_location": location_by_zip, 
            "input_income": input_income, 
            "input_size": input_amt,
            "input_footprint_housing_naturalgas_dollars": input_nat_gas_bill,
            "input_footprint_transportation_fuel1": input_fuel,
            "input_footprint_transportation_miles1": vehicle_travel,
            "input_footprint_transportation_mpg1": input_mpg,
            "input_footprint_transportation_bus": input_public_trans,
            "input_footprint_housing_electricity_dollars": input_elect_bill
            }
    headers = {"app_id": app_id, "app_key": app_key, "Accept": "application/xml" }
    
    response = requests.get("https://apis.berkeley.edu/coolclimate/footprint-defaults", params=payload, headers=headers)
    
    result = {}
   

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(response.content)
    for child in tree:
        for child in tree:
            if child.tag == 'input_location_mode':
                result['input_location_mode']= child.text
            if child.tag == 'input_location':
                result['input_location']= child.text
            
            if child.tag == 'input_income':
                result['input_income']= child.text
            
            if child.tag == 'input_size':
                result['input_size']= child.text
            
            if child.tag == 'input_footprint_housing_electricity_dollars':
                result['input_footprint_housing_electricity_dollars']= child.text        
            
            if child.tag == 'input_footprint_transportation_fuel1':
                result['input_footprint_transportation_fuel1']= child.text
            
            if child.tag == 'input_footprint_transportation_miles1':
                result['input_footprint_transportation_miles1']= child.text
            
            if child.tag == 'input_footprint_transportation_mpg1':
                result['input_footprint_transportation_mpg1']= child.text
            
            if child.tag == 'input_footprint_housing_naturalgas_dollars':
                result['input_footprint_housing_naturalgas_dollars']= child.text 

            if child.tag == 'input_footprint_transportation_bus':
                result['input_footprint_transportation_bus']= child.text
            
    return result


def existing_user_cc_calcs(user_id):
    """deliver user that already exists its calculations through the database"""
    
    user_obj = crud.get_user_by_id(user_id) 
    user_location = user_obj.household[0].zipcode 
    user_income = user_obj.household[0].income
 
    household_size = user_obj.household[0].num_occupants 
    elect_bill = user_obj.monthly_elect[0].elect_bill
    input_fuel = user_obj.vehicle[0].fuel_type
    vehicle_miles = user_obj.vehicle_travel[0].mileage
    input_mpg = user_obj.vehicle[0].mpg
    nat_gas_bill = user_obj.monthly_nat_gas[0].nat_gas_bill
    public_trans = user_obj.public_trans[0].mileage 
    
    results = coolclimate_defaults(user_location, input_fuel, input_mpg, vehicle_miles, public_trans, user_income, household_size, elect_bill, 
                       nat_gas_bill)
    
    return results
