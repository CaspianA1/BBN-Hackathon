import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import requests, json, datetime

app = Flask(__name__)
"""
Afraid
• Aggravated
• Angry
• Anxious
• Ashamed
• Assertive
• Burdened
• Brave
• Calm
• Cautious
• Challenged
• Cheerful
• Cherished
• Comforted
• Contented
• Creative
• Curious
• Depressed
• Embarrassed
• Energized
• Envious
• Excited
• Furious
• Guilty
• Grumpy
• Happy
• Hopeful
• Humiliated
• Hurt
• Indifferent
• Insecure
• Irritated
• Lonely
• Loved
• Mad
• Optimistic
• Overwhelmed
• Panicked
• Peaceful
• Positive
• Pessimistic
• Prepared
• Proud
• Ready for
change
• Regretful
• Relieved
• Renewed
• Sad
• Self-confident
• Shameful
• Skeptical
• Sorrowful
• Worried
"""
activity_group = """************ FOOD ************
MOOD: RELIEVED / CHERISHED / RENEWED / FANCY / HUNGRY / INDULGENT / COMFORTED / CURIOUS
ACTION: EAT
	bakery
	cafe
	meal_delivery
	meal_takeaway
	restaurant



************ STORE - CHILL ************
MOOD: CHILL / HAPPY / PEACEFUL / CALM
ACTION: BUYING
	bicycle_store
	book_store
	hardware_store
	home_goods_store
	convenience_store
	drugstore
	store
	liquor_store
	supermarket
	pharmacy



************ STORE - SHOPPING ************
MOOD: RELIEVED / CHALLENGED / ASSERTIVE / INTENSE / INDULGENT / HOPEFUL / INDULGENT / OVERWHELMED / CREATIVE
ACTION: SHOPPING
	shoe_store
	shopping_mall
	clothing_store
	department_store
	electronics_store
	furniture_store
	jewelry_store
	pet_store



********* BEAUTY ***********
MOOD: INDULGENT / RELIEVED / RELAX / PEACEFUL / CALM / CHERISHED / COMFORTED / POSITIVE / CONFIDENT / CREATIVE / HAPPY
ACTION: SIT BACK AND RELAX
	beauty_salon
	hair_care
	spa



************ TRANSPORTATION ************
MOOD: CHILL / RELAX / NONCHALANT / HOPEFUL
ACTION: HANG AROUND / SIT DOWN N TALK
	bus_station
	gas_station
	light_rail_station
	subway_station
	taxi_stand
	train_station
	transit_station
	parking



************ AMUSEMENT ************
MOOD: FUN / EXCITED / INTENSE / ENERGETIC / RELIEVED / HOPEFUL / CALM / COMFORTED / CURIOUS / CREATIVE / HAPPY
ACTION: RUN AROUND / GO CRAZY
	amusement_park
	bowling_alley



************ ENTERTAINMENT ************
MOOD: FUN / CHILL / RELIEVED / COMFORTED / CALM / CURIOUS / CREATIVE / HAPPY
ACTION: WATCH / RELAX, SIT BACK, AND ENJOY THE SHOW
	movie_rental
	movie_theater



************ SITES ************
MOOD: CHALLENGED / CHILL / EXCITED / HOPEFUL / EXPLORE / COMFORTED
ACTION: LOOK AT COOL STUFF
	aquarium
	art_gallery
	zoo
	museum
	tourist_attraction



************ PARTY ************
MOOD: FUN / CRAZY / EXCITED / EXPLORE / RELIEVED / CHALLENGED / CONFIDENT / CHERISHED / RENEWED / CURIOUS / CREATIVE / HAPPY
ACTION: DANCE / DRINK / GAMBLE
	bar
	casino
	night_club



************ OUTDOORS/ACTIVE ************
MOOD: FUN / NATURE / INTENSE / EXPLORE / RENEWED / CREATIVE
ACTION: HIKE / JOG / RUN / WALK / BIKE / WORKOUT / EXERCISE
	campground
	park
	gym



************ TOWN/GOVERNMENT LOCATIONS ************
MOOD: SERIOUS / CHILL / EXPLORE / CURIOUS
ACTION: WALK AROUND / CHILL / DO NOTHING
	city_hall
	courthouse
	fire_station
	police
	post_office
	local_government_office



************ SCHOOL/LEARNING ************
MOOD: SERIOUS / CALM / CHALLENGED / RENEWED / CREATIVE / CURIOUS
ACTION: WALK AROUND / READ / DO WORK / CHILL / RELAX
	school
	secondary_school
	primary_school
	university
	library"""

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

    def __repr__(self):
        return f"Activity {self.activity_id}: {self.activity_name} with description {self.description}"

class Placetype(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'Place Type {self.type_id}: {self.type_name}'

class Placetype_and_Activity(db.Model):
    connection_id = db.Column(db.Integer, primary_key=True)
    placetype_id = db.Column(db.Integer, nullable=False)
    activity_id = db.Column(db.Integer, nullable=False)

class Action_and_Activity(db.Model):
    connection_id = db.Column(db.Integer, primary_key=True)
    action_id = db.Column(db.Integer, nullable=False)
    activity_id = db.Column(db.Integer, nullable=False)

class Mood_and_Activity(db.Model):
    connection_id = db.Column(db.Integer, primary_key=True)
    mood_id = db.Column(db.Integer, nullable=False)
    activity_id = db.Column(db.Integer, nullable=False)

class Action(db.Model):
    action_id = db.Column(db.Integer, primary_key=True)
    action_name = db.Column(db.String, nullable=False)

class Mood(db.Model):
	mood_id = db.Column(db.Integer, primary_key=True)
	mood_name = db.Column(db.String, nullable=False)


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String, nullable=True, default="Anonymous")
    message = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Comment {self.comment_id} Written by {self.author_name} with message {self.message}"

def main():
	db.create_all()

	for place_type in s.split('\n'):
		new_type = Placetype(type_name=place_type.strip())
		db.session.add(new_type)
		db.session.commit()

	actions = set()

	moods = set()

	actions_to_activities = []

	moods_to_activites = []

	placetypes_to_activities = []

	for section in activity_group.replace('*', '').strip().split('\n\n\n'):
		section_name = section.strip().split('\n')[0].strip()
		new_activity = Activity(activity_name=section_name)
		db.session.add(new_activity)
		db.session.commit()
		new_actions = []
		new_moods = []
		for string in section.strip().split('\n')[2].lstrip('ACTION: ').strip().split('/'):
			new_actions.append(string.strip())
			actions_to_activities.append([string.strip(), new_activity.activity_id])
		

		for string in section.strip().split('\n')[1].strip('MOOD: ').strip().split('/'):
			new_moods.append(string.strip())
			moods_to_activites.append([string.strip(), new_activity.activity_id])


		actions = actions.union(set(new_actions))

		moods = moods.union(set(new_moods))

		placetype_list = [Placetype.query.filter_by(type_name=string.strip()).first().type_id for string in section.split('ACTION')[1].strip().split('\n')[1:] if len(string.strip()) > 0]
		
		placetypes_to_activities.extend([[pk, new_activity.activity_id] for pk in placetype_list])

	action_dictionary = {}
	for action in actions:
		new_action = Action(action_name=action)
		db.session.add(new_action)
		db.session.commit()
		action_dictionary[action] = new_action.action_id

	mood_dictionary = {}
	for mood in moods:
		new_mood = Mood(mood_name=mood)
		db.session.add(new_mood)
		db.session.commit()
		mood_dictionary[mood] = new_mood.mood_id
	
	for connection in placetypes_to_activities:
		new_connection = Placetype_and_Activity(placetype_id=connection[0], activity_id=connection[1])
		db.session.add(new_connection)
		db.session.commit()

	for connection in moods_to_activites:
		new_connection = Mood_and_Activity(mood_id=mood_dictionary[connection[0]], activity_id=connection[1])
		db.session.add(new_connection)
		db.session.commit()
	
	for connection in actions_to_activities:
		new_connection = Action_and_Activity(action_id=action_dictionary[connection[0]], activity_id=connection[1])
		db.session.add(new_connection)
		db.session.commit()



if __name__=='__main__':
	main()







