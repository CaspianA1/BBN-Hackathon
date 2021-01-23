import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import requests, json, datetime

app = Flask(__name__)

s = """accounting
airport
amusement_park
aquarium
art_gallery
atm
bakery
bank
bar
beauty_salon
bicycle_store
book_store
bowling_alley
bus_station
cafe
campground
car_dealer
car_rental
car_repair
car_wash
casino
cemetery
church
city_hall
clothing_store
convenience_store
courthouse
dentist
department_store
doctor
drugstore
electrician
electronics_store
embassy
fire_station
florist
funeral_home
furniture_store
gas_station
gym
hair_care
hardware_store
hindu_temple
home_goods_store
hospital
insurance_agency
jewelry_store
laundry
lawyer
library
light_rail_station
liquor_store
local_government_office
locksmith
lodging
meal_delivery
meal_takeaway
mosque
movie_rental
movie_theater
moving_company
museum
night_club
painter
park
parking
pet_store
pharmacy
physiotherapist
plumber
police
post_office
primary_school
real_estate_agency
restaurant
roofing_contractor
rv_park
school
secondary_school
shoe_store
shopping_mall
spa
stadium
storage
store
subway_station
supermarket
synagogue
taxi_stand
tourist_attraction
train_station
transit_station
travel_agency
university
veterinary_care
zoo"""

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackathon2021.db'
db = SQLAlchemy(app)
app.secret_key = 'somethingsecret'
app.config["SESSION_TYPE"] = 'filesystem'

class Activity(db.Model):
    activity_id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True, default="")
    included_types = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Activity {self.activity_id}: {self.activity_name} with description {self.description}"

class Placetype(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'Place Type {self.type_id}: {self.type_name}'


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String, nullable=True, default="Anonymous")
    message = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Comment {self.comment_id} Written by {self.author_name} with message {self.message}"

db.create_all()

for place_type in s.split('\n'):
    new_type = Placetype(type_name=place_type.strip())
    db.session.add(new_type)
    db.session.commit()