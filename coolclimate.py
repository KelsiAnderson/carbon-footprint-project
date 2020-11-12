import os
import requests

app_id = os.environ['app_id']
app_key = os.environ['app_key']

def coolclimate_defaults(input_fuel, input_mpg, vehicle_travel, input_public_trans, input_income, input_amt,
                    input_elect_bill, input_nat_gas_bill):
    #add header and refer to variables app_id and app_key not actual keys
    #params/payload
    #request.get from below
    #connect user response
    url = "https://apis.berkeley.edu/coolclimate/footprint-sandbox"
    payload = {'input_income': input_income, 
            'input_footprint_transportation_miles1': vehicle_travel, 
            'input_footprint_transportation_fuel1': input_fuel, 
            'input_footprint_transportation_mpg1': input_mpg, 
            'input_size': input_amt,
            'input_footprint_transportation_mpg1': input_public_trans
            # 'input_natural_gas_monthly_bill': input_nat_gas_bill,
            # 'input_elctricity_monthly_bill': input_elect_bill
            }
            #coolclimate_defaults('gas', 32, 12000, 100, 6, 2, 32.00, 10.00)
    #print(payload)
    headers = {"app_id": app_id, "app_key": app_key, "Accept": "application/xml" }
    
    response = requests.get("https://apis.berkeley.edu/coolclimate/footprint-sandbox", params=payload, headers=headers)
    #print(response.text)
    #data = response.json()
    #print(data)
    # income = data['_embedded']['input_income']
    # vehicle_miles = data['_embdedded']['input_footprint_transportation_miles1']
    # vehicle_fuel = data['_embdeed']['input_footprint_transportation_fuel1']
    return response

response = coolclimate_defaults("gas", 32, 13000, 100, 6, 2, 32.00, 10.00 )

from xml.etree import ElementTree
tree = ElementTree.fromstring(response.content)
for child in tree:
    print(child.tag, child.text)
    #turne child.text into dictionary
    #extract the info needed from child.text
    #