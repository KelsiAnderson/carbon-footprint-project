
"""CRUD operations"""

from model import db, User, Vehicle, Vehicle_Travel, Public_Trans, Household, Monthly_Nat_Gas, Monthly_Elect, Comments, connect_to_db
from datetime import datetime


def create_user(fname, user_name, email, password):
    """Create and return a new user"""

    user = User(fname=fname, user_name=user_name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

#THIS TABLE IS DELETED. Obsolete?
# def create_location(zipcode, user_id):

#     location = Location(zipcode=zipcode, user_id=user_id)

#     db.session.add(location)
#     db.session.commit()

#     return location
    


def create_vehicle(mpg, fuel_type, user_id):
    """create and return a new users vehicle"""
    mileage = Vehicle(mpg=mpg, fuel_type=fuel_type, user_id= user_id)

    db.session.add(mileage)
    db.session.commit()

    return mileage


def create_vehicle_travel(mileage, travel_date, carbon_footprint, user_id, vehicle_id):
    """create and return daily travel by vehicle """

    daily_travel = Vehicle_Travel(mileage=mileage, travel_date=travel_date, carbon_footprint=carbon_footprint, user_id=user_id, vehicle_id=vehicle_id)

    db.session.add(daily_travel)
    db.session.commit()

    return daily_travel

def create_public_trans(mileage, public_trans_date, carbon_footprint, user_id):
    """create and return daily public transit"""

    public_trans = Public_Trans(mileage=mileage, public_trans_date=public_trans_date, carbon_footprint=carbon_footprint, user_id=user_id)

    db.session.add(public_trans)
    db.session.commit()

    return public_trans

def create_household(num_occupants, income, zipcode, user_id):
    """create and return household"""
    
    household = Household(num_occupants=num_occupants, income=income, zipcode=zipcode, user_id=user_id)

    db.session.add(household)
    db.session.commit()

    return household


def create_monthly_nat_gas(nat_gas_bill, nat_gas_date, carbon_footprint, user_id, household_id):
    """create and return the monthly gass bill"""

    monthly_gas_bill = Monthly_Nat_Gas(nat_gas_bill=nat_gas_bill, nat_gas_date=nat_gas_date, carbon_footprint=carbon_footprint, user_id=user_id, household_id=household_id)

    db.session.add(monthly_gas_bill)
    db.session.commit()

    return monthly_gas_bill

def create_monthly_elect_bill(elect_bill, elect_date, carbon_footprint, user_id, household_id):
    """create and return monthly electricity use"""

    monthly_elect_bill = Monthly_Elect(elect_bill=elect_bill, elect_date=elect_date, carbon_footprint=carbon_footprint, user_id=user_id, household_id=household_id)

    db.session.add(monthly_elect_bill)
    db.session.commit()

    return monthly_elect_bill


def create_comment(text, user_id):
    """create and return a users comments"""

    comments = Comments(text=text, user_id=user_id)

    db.session.add(comments)
    db.session.commit()

    return comments


def all_users():
    """get and return all users"""
    return user.query.all()


def get_user_by_id(user_id):
    """get user by user id"""
    
    user_by_id = User.query.get(user_id)
    return user_by_id


def get_user_by_email(email):
    """get and return users by email address"""
    
    return User.query.filter(User.email == email).first()

# def get_location(zipcode):

#     return Household.query.filter(Household.zipcode == zipcode).first()


def get_vehicle_by_id(vehicle_id):
    """get and return vehicle type by id"""

    vehicle_by_id = Vehicle.query.get(vehicle_id)
    return vehicle_by_id

def get_monthly_nat_gas_by_user(user_id):

    gas_by_bill = Monthly_Nat_Gas.query.filter(Monthly_Nat_Gas.user_id == user_id).first()
    return gas_by_bill

def get_monthly_elect_by_user(user_id):

    monthly_elect = Monthly_Elect.query.filter(Monthly_Elect.user_id == user_id).first()
    return monthly_elect

def get_vehicle_travel_by_user(user_id):

    vehicle_travel = Vehicle_Travel.query.filter(Vehicle_Travel.user_id == user_id).first()
    return vehicle_travel

def add_mileage(user_id, mileage, carbon_footprint, travel_date=datetime.now()):

    add_mileage = Vehicle_Travel(user_id=user_id, mileage=mileage, carbon_footprint=carbon_footprint, travel_date=travel_date)
    db.session.add(add_mileage)
    db.session.commit()

    return add_mileage

def add_household_info(user_id, input_amt, input_income, location_by_zip):

    add_house_info = Household(num_occupants=input_amt, income=input_income, zipcode=location_by_zip, user_id=user_id)
    db.session.add(add_house_info)
    db.session.commit()

    return add_house_info

def add_vehicle_info(input_fuel, input_mpg, user_id):

    seed_vehicle_info = Vehicle(fuel_type=input_fuel, mpg=input_mpg, user_id=user_id)
    db.session.add(seed_vehicle_info)
    db.session.commit()

    return seed_vehicle_info

def add_public_trans(user_id, input_public_trans, carbon_footprint, travel_date=datetime.now()):
    
    seed_public_trans = Public_Trans(mileage=input_public_trans, user_id=user_id, carbon_footprint=carbon_footprint, public_trans_date=travel_date)
    db.session.add(seed_public_trans)
    db.session.commit()

    return seed_public_trans

def add_elect_bill(user_id, input_elect_bill, carbon_footprint, travel_date=datetime.now()):
 
    seed_elect_info = Monthly_Elect(elect_bill=input_elect_bill, carbon_footprint=carbon_footprint, user_id=user_id, elect_date=travel_date)
    db.session.add(seed_elect_info)
    db.session.commit()

    return seed_elect_info

def add_nat_gas_info(input_nat_gas_bill, carbon_footprint, user_id, travel_date=datetime.now()):

    seed_nat_gas_info = Monthly_Nat_Gas(nat_gas_bill=input_nat_gas_bill, carbon_footprint=carbon_footprint, user_id=user_id, nat_gas_date=travel_date)
    db.session.add(seed_nat_gas_info)
    db.session.commit()

    return seed_nat_gas_info

def change_vehicle_carbon(user_id, vehicle_emit):

    vehicle_carbon = Vehicle_Travel.query.get(user_id)
    vehicle_carbon.carbon_footprint = vehicle_emit
    db.session.commit()

    return vehicle_carbon

def change_gas_carbon(user_id, nat_gas_emit):

    gas_carbon = Monthly_Nat_Gas.query.get(user_id)
    gas_carbon.carbon_footprint = nat_gas_emit
    db.session.commit()

    return gas_carbon

def change_elect_carbon(user_id, elect_emit):

    elect_carbon = Monthly_Elect.query.get(user_id)
    elect_carbon.carbon_footprint = elect_emit
    db.session.commit()

    return elect_carbon

def change_public_trans_carbon(user_id, public_trans_emit):

    public_trans_carbon = Public_Trans.query.get(user_id)
    public_trans_carbon.carbon_footprint = public_trans_emit
    db.session.commit()

    return public_trans_carbon


def compare_monthly_elect(user_id, month, year):
    
    first_of_month = datetime(year=year, month=month, day=1)
    last_of_month = datetime(year=year, month=(month + 1), day=1)
    current_date = Monthly_Elect.query.filter((Monthly_Elect.elect_date >= first_of_month), (Monthly_Elect.elect_date < last_of_month)).all()
    #print("CHECK OUT THE CURRENT DATE", current_date)
    
    sum = 0
    for dates in current_date:
        sum += dates.carbon_footprint

    return sum

def compare_monthly_nat_gas(user_id, month, year):

    first_of_month = datetime(year=year, month=month, day=1)
    last_of_month = datetime(year=year, month=(month + 1), day=1)
    current_date = Monthly_Nat_Gas.query.filter((Monthly_Nat_Gas.nat_gas_date >= first_of_month), (Monthly_Nat_Gas.nat_gas_date < last_of_month)).all()
    #print("CHECK OUT THE CURRENT DATE", current_date)

    sum = 0
    for dates in current_date:
        sum += dates.carbon_footprint

        return sum

def compare_monthly_vehicle_emissions(user_id, month, year):

    first_of_month = datetime(year=year, month=month, day=1)
    last_of_month = datetime(year=year, month=(month + 1), day=1)
    current_date = Vehicle_Travel.query.filter((Vehicle_Travel.travel_date >= first_of_month), (Vehicle_Travel.travel_date < last_of_month)).all()
    #print("CHECK OUT THE CURRENT DATE", current_date)

    sum = 0
    for dates in current_date:  
        sum += dates.carbon_footprint

    return sum

def compare_monthly_public_trans(user_id, month, year):
    
    first_of_month = datetime(year=year, month=month, day=1)
    last_of_month = datetime(year=year, month=(month + 1), day=1)
    current_date = Public_Trans.query.filter((Public_Trans.public_trans_date >= first_of_month), (Public_Trans.public_trans_date < last_of_month)).all()
    print("CHECK OUT THE CURRENT DATE", current_date)

    sum = 0
    for dates in current_date:  
        sum += dates.carbon_footprint

    return sum




def get_household_by_id(user_id):

    household = Household.query.filter(Vehicle_Travel.user_id == user_id).first()
    return household


if __name__ == '__main__':
    from server import app
    connect_to_db(app)  