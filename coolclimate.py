import os
import requests

app_id = os.environ['app_id']
app_key = os.environ['app_key']

def coolclimate_defaults(location_by_zip, input_fuel, input_mpg, vehicle_travel, input_public_trans, input_income, input_amt,
                    input_elect_bill, input_nat_gas_bill):
    #add header and refer to variables app_id and app_key not actual keys
    #params/payload
    #request.get from below
    #connect user response



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
        print(child.tag, child.text)
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
            
    print(result)
    return result

response = coolclimate_defaults(location_by_zip=80120, input_fuel="gas", input_mpg=32, vehicle_travel=13000, input_public_trans=100, input_income=6, input_amt=2,
                    input_elect_bill=30.00, input_nat_gas_bill=22.00)


##############################################################
# def existing_user_cc_calcs(user_id):
#     """deliver user that already exists its calculations through the database"""
#     user_obj = User.query.filter(user_id=user_id)
#     user_location = user_obj.location.zipcode