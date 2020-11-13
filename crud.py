
"""CRUD operations"""

from model import db, User, Location, Vehicle, Vehicle_Travel, Public_Trans, Household, Monthly_Nat_Gas, Monthly_Elect, Comments, connect_to_db

def create_user(fname, user_name, email, password):
    """Create and return a new user"""

    user = User(fname=fname, user_name=user_name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_location(zipcode, user_id):

    location = Location(zipcode=zipcode, user_id=user_id)

    db.session.add(location)
    db.session.commit()

    return location
    


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

def create_household(num_occupants, income, user_id):
    """create and return household"""
    
    household = Household(num_occupants=num_occupants, income=income, user_id=user_id)

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

def get_location(zipcode):

    return Location.query.filter(Location.zipcode == zipcode).first()

# def get_fuel(fuel_type):


#     return Vehicle.query.filter(Vehicle.fuel_type == fuel_type).first()

def get_mpg(mpg):

    return Vehicle.query.filter(Vehicle.mpg == mpg).first()

def get_public_trans(mileage):
    
    return Public_Trans.query.filter(Public_Trans.mileage == mileage).first()

def get_user_income(income):

    return Household.query.filter(Household.income == income).first()

def get_num_occupants(num_occupants):

    return Household.query.filter(Household.num_occupants == num_occupants).first()

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

def add_user_info(location_by_zip, input_fuel, input_mpg, vehicle_travel, input_public_trans, 
            input_income, input_amt, input_elect_bill, input_nat_gas_bill, user_id):

    add_location = Location(zipcode=location_by_zip, user_id=user_id)
    db.session.add(add_location)
    db.session.commit()


    add_fuel = Vehicle(fuel_type=input_fuel, mpg=input_mpg, user_id=user_id)
    db.session.add(add_fuel)
    db.session.commit()

    add_vehicle_travel = Vehicle_Travel(mileage=vehicle_travel, user_id=user_id)
    db.session.add(add_vehicle_travel)
    db.session.commit()

    add_public_trans = Public_Trans(mileage=input_public_trans, user_id=user_id)
    db.session.add(add_fuel)
    db.session.commit()

    add_income = Household(income=input_income, num_occupants=input_amt, user_id=user_id)
    db.session.add(add_income)
    db.session.commit()

    add_elect_bill = Monthly_Elect(elect_bill=input_elect_bill, user_id=user_id)
    db.session.add(add_elect_bill)
    db.session.commit()

    add_nat_gas = Monthly_Nat_Gas(nat_gas_bill=input_nat_gas_bill, user_id=user_id)
    db.session.add(add_nat_gas)
    db.session.commit()

    return "success!"

#TODO: create a route for household income
def get_household_by_id(user_id):

    household = Household.query.filter(vehicle_Travel.user_id == user_id).first()
    return household

if __name__ == '__main__':
    from server import app
    connect_to_db(app)  