import unittest

from server import app
from model import db, connect_to_db, User, Vehicle, Vehicle_Travel, Public_Trans, Household, Monthly_Nat_Gas, Monthly_Elect 
from datetime import datetime


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    Monthly_Elect.query.delete()
    Monthly_Nat_Gas.query.delete()
    Household.query.delete()
    Public_Trans.query.delete()
    Vehicle_Travel.query.delete()
    Vehicle.query.delete()    
    User.query.delete()


    new_user = User(user_id= 50, fname="Karen", user_name = "KarenK", email = "Karen@Karen", 
    password = "hiimKaren12")
    new_vehicle = Vehicle(fuel_type = 1, mpg = 32, user = new_user)
    new_vehicle_travel = Vehicle_Travel(mileage = 12000, travel_date = datetime.now(), carbon_footprint = 14000, user = new_user, vehicle = new_vehicle)
    new_public_trans = Public_Trans(mileage = 300, public_trans_date = datetime.now(), carbon_footprint = 88.75, user = new_user)
    new_household = Household(num_occupants = 3, income = 5, zipcode = 80123, user = new_user)
    new_monthly_gas = Monthly_Nat_Gas(nat_gas_bill = 35.00,nat_gas_date= datetime.now(), carbon_footprint = 460, user = new_user, household = new_household)
    new_monthly_elect = Monthly_Elect(elect_bill = 200.00, elect_date = datetime.now(), carbon_footprint = 530, household = new_household, user = new_user)


    user_bob = User(user_id = 51, fname="Bob", user_name = "BobB", email = "bob@bob", 
    password = "hiimbob12")
    vehicle_bob = Vehicle(fuel_type = 1, mpg = 22, user = user_bob)
    vehicle_travel_bob = Vehicle_Travel(mileage = 10000, travel_date = datetime.now(), carbon_footprint = 12000, user = user_bob, vehicle = vehicle_bob)
    public_trans_bob = Public_Trans(mileage = 600, public_trans_date = datetime.now(), carbon_footprint = 90.75, user = user_bob)
    household_bob = Household(num_occupants = 2, income = 4, zipcode = 80120, user = user_bob)
    monthly_gas_bob = Monthly_Nat_Gas(nat_gas_bill = 25.00,nat_gas_date= datetime.now(), carbon_footprint = 460, user = user_bob, household = household_bob)
    monthly_elect_bob = Monthly_Elect(elect_bill = 150.00, elect_date = datetime.now(), carbon_footprint = 510, household = household_bob, user = user_bob)



    db.session.add_all([new_user, new_vehicle, new_vehicle_travel, new_public_trans, new_household, 
        new_monthly_gas, new_monthly_elect, user_bob, vehicle_bob, vehicle_travel_bob,
        public_trans_bob, household_bob, monthly_gas_bob, monthly_elect_bob])
    
    db.session.commit()


# class can be naemd whatever, TastCase is opting in to test set up and run test behavior
#this makes it clear for others reading the code because it follows the norm/consistent pattern that it is testing. 

class EmissionTests(unittest.TestCase):
    """stuff to do before every test"""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 50
        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def test_homepage(self):
        result = self.client.get("/")
        print("SEE DATA", result.data)
        self.assertIn(b'<h2>LEARN MORE ABOUT YOUR CARBON IMPACT!</h2>', result.data)

        print("HI AM I WORKING?")
    #ui test? testing for presence of things on page (assertIn)
    def test_profile(self):
        result = self.client.get("/existing_users?email=Kelsi&password=1234")
        print("PROFILE DATA", result.data)
        self.assertIn(b"<h3>Check out your emissions for this month by category:</h3>", result.data)

        print("DOES THIS WORK?")

    def test_new_account(self):
        result = self.client.get("/existing_users")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<p>Don't have an account?</p>", result.data)
        self.assertNotIn(b"<h2>LOGIN</h2>", result.data)

        print("DO I WORK?")

if __name__ == "__main__":
    import unittest
    
    unittest.main()