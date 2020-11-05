"""script to seed the database"""

import os
import json
from random import choice, randint
from datetime import datetime
from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db
import crud


import crud
import model
import server

# os.sysytem('dropdb ratings')
# os.system('createdb ratings')

# model.connect_to_db(server.app)
# model.db.create_all()

#for element in list, create user password
def open_pipe_file(pipe_file): 
    with open(pipe_file) as open_file:
        result_list = []

        for line in open_file:
            #print(line)
            result_list.append(line.rstrip().split('|'))

    return result_list


comments_list = open_pipe_file("seed_text_files/comments.seed")

for comment in comments_list:
    comment_id = comment[0]
    user_id = comment[1]
    text = comment[2]
    all_comments = crud.create_comment(comment_id, user_id, text)
    
