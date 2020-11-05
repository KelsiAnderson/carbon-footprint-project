
"""CRUD operations"""

from model import db, user, vehicle, vehicle_travel, public_trans, household, monthly_nat_gas, monthly_elect, comments

def create_user(email, password):
    """Create and return a new user"""

    user = user(emal=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_vehicle(mpg):
    """create and return a new users vehicle"""
    mileage = vehicle(mpg=mpg)

    db.session.add(mileage)
    db.session.commit()

    return mileage


def create_vehicle_travel(mileage, travel_date, carbon_footprint):
    """create and return daily travel by vehicle """

    daily_travel = vehicle_travel(pileage=mileage, tavel_date=travel_date, carbon_footprint=carbon_footprint)

    db.session.add(daily_travel)
    db.session.commit()

    return daily_travel

def create_public_trans(mileage, public_trans_date, carbon_footprint):
    """create and return daily public transit"""

    public_trans = public_trans(mileage=mileage, public_trans_date=public_trans_datem carbon_footprint=carbon_footprint)

    db.session.add(public_trans)
    db.session.commit()

    return public_trans

def create_household(num_occupants):
    """create and return household"""
    
    num_occupants = household(num_occupants=num_occupants)

    db.session.add(num_occupants)
    db.session.commit()

    return num_occupants


def create_monthly_nat_gas(nat_gas_bill, nat_gas_date, carbon_footprint):
    """create and return the monthly gass bill"""

    monthly_gas_bill = monthly_nat_gas(nat_gas_bill=nat_gas_bill, nat_gas_date=nat_gas_date, carbon_footprint=carbon_footprint)

    db.session.add(monthly_gas_bill)
    db.session.commit()

    return monthly_gas_bill

def create_montly_elect_bill(elect_bill, elect_date, carbon_footprint):
    """create and return monthly electricity use"""

    monthly_elect_bill = monthly_elect(elect_bill=elect_bill, elect_date=elect_date, carbon_footprint=carbon_footprint)

    db.session.add(monthly_elect_bill)
    db.session.commit()

    return monthly_elect_bill

def comments(text):
    """create and return a users comments"""

    comments = comments(text=text)

    db.session.add(comments)
    db.session.commit()

    return comments

def all_users():
    """get and return all users"""
    return user.query.all()


def get_user_by_id(user_id):
    """get user by user id"""
    
    user_by_id = user.query.get(user_id)
    return user_by_id

def get_user_by_email(email):
    """get and return users by email address"""

    return user.query.filter(user.email == email).first()

def get vehicle_by_id(vehicle_id):
    """get and return vehicle type by id"""

    vehicle_by_id = vehicle.query.get(vehicle_id)
    return vehicle_by_id

if __name__ == '__main__':
    from server import app
    connect_to_db(app)