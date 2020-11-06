"""script to seed the database"""

import os
from random import choice, randint
from datetime import datetime
from flask import (Flask, render_template, request, flash, session, redirect)
from server import app
from model import connect_to_db, db, User, Vehicle, Vehicle_Travel, Public_Trans, Household, Monthly_Nat_Gas, Monthly_Elect, Comments

import crud


import crud
import model
import server

# os.sysytem('dropdb ratings')
# os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

#for element in list, create user password
def open_pipe_file(pipe_file): 
    with open(pipe_file) as open_file:
        result_list = []

        for line in open_file:
            #print(line)
            result_list.append(line.rstrip().split('|'))

    return result_list


user_file = open_pipe_file("seed_text_files/user.seed")
for user in user_file:
    user_name = user[0] 
    email = user[1]
    password = user[2]
    all_users = crud.create_user(user_name, email, password)


vehicle_file = open_pipe_file("seed_text_files/vehicle.seed")
for vehicle in vehicle_file:
    mpg = vehicle[0]
    all_vehicles = crud.create_vehicle(mpg)

vehicle_travel_file = open_pipe_file("seed_text_files/vehicle_travel.seed")
for travel in vehicle_travel_file:
    mileage = travel[0]
    travel_date = travel[1]
    carbon_footprint - travel[2]
    vehicle_travel = crud.create_vehicle_travel(mileage, travel_date, carbon_footprint)

