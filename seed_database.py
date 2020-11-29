"""script to seed the database"""

import os
from random import choice, randint
from datetime import datetime
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db, User, Vehicle, Vehicle_Travel, Public_Trans, Household, Monthly_Nat_Gas, Monthly_Elect, Comments

import crud
from server import app

connect_to_db(app)
db.create_all()

#for element in list, create user password
def open_pipe_file(pipe_file): 
    with open(pipe_file) as open_file:
        result_list = []

        for line in open_file:
            result_list.append(line.rstrip().split('|'))

    return result_list


user_file = open_pipe_file("seed_text_files/user.seed")
for user in user_file:
    fname, user_name, email, password = user
    all_users = crud.create_user(fname, user_name, email, password)

vehicle_file = open_pipe_file("seed_text_files/vehicle.seed")
for vehicle in vehicle_file:
    mpg, fuel_type, user_id = vehicle
    all_vehicles = crud.create_vehicle(mpg, fuel_type, user_id)

vehicle_travel_file = open_pipe_file("seed_text_files/vehicle_travel.seed")
for travel in vehicle_travel_file:
    mileage, travel_date, carbon_footprint, user_id, vehicle_id = travel
    all_v_travel = crud.create_vehicle_travel(mileage, travel_date, carbon_footprint, user_id, vehicle_id)

public_trans_file = open_pipe_file("seed_text_files/public_transit.seed")
for transit in public_trans_file:
    mileage, public_trans_date, carbon_footprint, user_id = transit
    transit_travel = crud.create_public_trans(mileage, public_trans_date, carbon_footprint, user_id)

household_file = open_pipe_file("seed_text_files/household.seed")
for house in household_file:
    num_occupants, income, zipcode, user_id = house
    household = crud.create_household(num_occupants, income, zipcode, user_id)

nat_gas_file = open_pipe_file("seed_text_files/nat_gas.seed")
for nat_gas in nat_gas_file:
    nat_gas_bill, nat_gas_date, carbon_footprint, user_id, household_id = nat_gas
    nat_gas_all = crud.create_monthly_nat_gas(nat_gas_bill, nat_gas_date, carbon_footprint, user_id, household_id)

monthly_elect_file = open_pipe_file("seed_text_files/electricity.seed")
for elect in monthly_elect_file:
    elect_bill, elect_date, carbon_footprint, user_id, household_id = elect
    monthly_elect = crud.create_monthly_elect_bill(elect_bill, elect_date, carbon_footprint, user_id, household_id)

comment_file = open_pipe_file("seed_text_files/comments.seed")
for comment in comment_file:
    text, user_id = comment
    comment_all = crud.create_comment(text, user_id)


# if __name__ == '__main__':
#     from server import app
#     connect_to_db(app) 