"""data models for my carbon emmissions app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """ table representing a user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fname = db.Column(db.String)
    user_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    # this has a foreign key for vehicle, daily vehicile travel, public trans, 
    #comment, household, monthly natural gas, monrthly elct use
    # location = db.relationship("Location")
    vehicle = db.relationship("Vehicle")
    vehicle_travel = db.relationship("Vehicle_Travel")
    public_trans = db.relationship("Public_Trans")
    monthly_nat_gas = db.relationship("Monthly_Nat_Gas")
    household = db.relationship("Household")
    monthly_elect = db.relationship("Monthly_Elect")
    comment = db.relationship("Comments")

    def __repr__(self):
        return f'<User user_id= {self.user_id} email={self.email}>'


class Vehicle(db.Model):
    """table representing the vehicle type a user drives"""

    __tablename__ = "vehicles"

    vehicle_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fuel_type = db.Column(db.Integer)
    mpg = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('User')

    def __repr__(self):
        return f'<vehicle vehicle_id={self.vehicle_id} user_id={self.user_id}>'

class Vehicle_Travel(db.Model):
    """table representing daily mileage travelled"""

    __tablename__ = "vehicle_travel"

    travel_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    mileage = db.Column(db.Integer)
    travel_date = db.Column(db.DateTime)
    carbon_footprint = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.vehicle_id'))
    

    user = db.relationship("User")
    vehicle = db.relationship("Vehicle")

    def __repr__(self):
        return f'<travel_id = {self.travel_id} mileage = {self.mileage}  vehicle_id = {self.vehicle_id} user_id = {self.user_id}>'

class Public_Trans(db.Model):
    """table to hold a users public transit travel"""

    __tablename__ = "public_transit"

    public_trans_id = db.Column(db.Integer, autoincrement= True, nullable= False, primary_key = True)
    mileage = db.Column(db.Integer)
    public_trans_date = db.Column(db.DateTime)
    carbon_footprint = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    

    user = db.relationship('User')

    def __repr__(self):
        return f'<public_trans_id = {self.public_trans_id} mileage = {self.mileage} user_id = {self.user_id}>'

class Household(db.Model):
    """table to represent household occupant amt"""

    __tablename__ = "households"

    household_id = db.Column(db.Integer, autoincrement = True, nullable = False, primary_key = True)
    num_occupants = db.Column(db.Integer)
    income = db.Column(db.Integer)
    zipcode = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('User')
    monthly_gas = db.relationship('Monthly_Nat_Gas')
    monthly_elect = db.relationship('Monthly_Elect')

    def __repr__(self):
        return f'<household_id  = {self.household_id } user_id = {self.user_id}>'

class Monthly_Nat_Gas(db.Model):
    """table to represent monthly gas use by bill amt"""

    __tablename__ = "natural_gas_usage"

    nat_gas_id = db.Column(db.Integer, autoincrement= True, nullable= False, primary_key = True)
    nat_gas_bill = db.Column(db.Float)
    nat_gas_date = db.Column(db.DateTime)
    carbon_footprint = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    household_id = db.Column(db.Integer, db.ForeignKey('households.household_id'))

    user = db.relationship('User')
    household = db.relationship('Household')

    def __repr__(self):
        return f'<nat_gas_id = {self.nat_gas_id} nat_gas_date = {self.nat_gas_date} user_id = {self.user_id}>'

class Monthly_Elect(db.Model):
    """table representing monthly elcetricity use by bill amt"""

    __tablename__ = "electricity_use"

    elect_id = db.Column(db.Integer, autoincrement = True, nullable = False, primary_key = True)
    elect_bill = db.Column(db.Float)
    elect_date = db.Column(db.DateTime)
    carbon_footprint = db.Column(db.Float)
    household_id = db.Column(db.Integer, db.ForeignKey('households.household_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('User')
    household = db.relationship('Household')

    def __repr__(self):
        return f'<electricity_id = {self.elect_id} elect_bill = {self.elect_bill} electricity_date = {self.elect_date} user_id = {self.user_id}>'

class Comments(db.Model):
    """table holding a users comments"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    text = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('User')

    def __repr__(self):
        return f'<comment_id = {self.comment_id} user_id = {self.user_id}>'



#Dont forget to turn on echo (echo = True)
def connect_to_db(flask_app, db_uri='postgresql:///project', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)



    print('Connect to the db!')

if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)