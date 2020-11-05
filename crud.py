
"""CRUD operations"""

from model import db, User, Vehicle, Vehicle_Travel, Public_Trans, Household, Monthly_Nat_Gas, Monthly_Elect, Comments, connect_to_db

def create_user(email, password):
    """Create and return a new user"""

    user = User(emal=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_vehicle(mpg):
    """create and return a new users vehicle"""
    mileage = Vehicle(mpg=mpg)

    db.session.add(mileage)
    db.session.commit()

    return mileage


def create_vehicle_travel(mileage, travel_date, carbon_footprint):
    """create and return daily travel by vehicle """

    daily_travel = Vehicle_Travel(pileage=mileage, tavel_date=travel_date, carbon_footprint=carbon_footprint)

    db.session.add(daily_travel)
    db.session.commit()

    return daily_travel

def create_public_trans(mileage, public_trans_date, carbon_footprint):
    """create and return daily public transit"""

    public_trans = Public_Trans(mileage=mileage, public_trans_date=public_trans_date, carbon_footprint=carbon_footprint)

    db.session.add(public_trans)
    db.session.commit()

    return public_trans

def create_household(num_occupants):
    """create and return household"""
    
    num_occupants = Household(num_occupants=num_occupants)

    db.session.add(num_occupants)
    db.session.commit()

    return num_occupants


def create_monthly_nat_gas(nat_gas_bill, nat_gas_date, carbon_footprint):
    """create and return the monthly gass bill"""

    monthly_gas_bill = Monthly_Nat_Gas(nat_gas_bill=nat_gas_bill, nat_gas_date=nat_gas_date, carbon_footprint=carbon_footprint)

    db.session.add(monthly_gas_bill)
    db.session.commit()

    return monthly_gas_bill

def create_montly_elect_bill(elect_bill, elect_date, carbon_footprint):
    """create and return monthly electricity use"""

    monthly_elect_bill = Monthly_Elect(elect_bill=elect_bill, elect_date=elect_date, carbon_footprint=carbon_footprint)

    db.session.add(monthly_elect_bill)
    db.session.commit()

    return monthly_elect_bill

def create_comment(comment_id, user_id, text):
    """create and return a users comments"""

    comments_instance = Comments(comment_id=comment_id, user_id=user_id, text=text)

    db.session.add(comments_instance)
    db.session.commit()

    return comments_instance

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

def get_vehicle_by_id(vehicle_id):
    """get and return vehicle type by id"""

    vehicle_by_id = Vehicle.query.get(vehicle_id)
    return vehicle_by_id

if __name__ == '__main__':
    from server import app
    connect_to_db(app)  