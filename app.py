import os
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from db_construction import Activity, Placetype, Comment, Action, Mood_and_Activity, Mood
from helper import vector_cosine_similarity, getPlaces
from activity_filter import nearby_locs_from_type
import requests, json, datetime, nltk, ssl, spacy, en_core_web_md, math

try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	pass
else:
	ssl._create_default_https_context = _create_unverified_https_context


nlp = en_core_web_md.load()

app = Flask(__name__)

with open('config.json') as json_data:
	config_file = json.load(json_data)

API_KEY = config_file['apikey']

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackathon2021.db'
db = SQLAlchemy(app)
app.secret_key = config_file['secretkey']
app.config["SESSION_TYPE"] = 'filesystem'


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method =='GET':# Activity.query.order_by(Activity.activity_name).all()
		return render_template("index.html", activities=Activity.query.order_by(Activity.activity_name).all(), results=False)
	else:
		#checklist will be all the selected activites
		checkList = []
		if request.form.get('activityCheck') == 'on':
			for activity_check in request.form.keys():
				if 'typeCheck' in activity_check and request.form.get(activity_check) == 'on':
					checkList.append(activity_check.split('@')[1].strip())
		radius = 10000
		if request.form.get('radiusCheck') == 'on':
			try:
				radius = int(request.form.get('radiusFilter')) * 1000
			except:
				pass
		price_range = None
		if request.form.get('priceCheck') == 'on':
			price_range = int(request.form.get('priceRange')) -1
		
		prefer_indoor = None
		if not int(request.form.get('indoorFilter')) == 3:
			prefer_indoor = (int(request.form.get('indoorFilter')) == 1)

		placetypes = getPlaces(checkList)

		#TODO: GOOGLE API filter by placetypes, radius, price range, and indoor?

		d = {'radius':radius}

		if len(checkList) > 0:
			d['type'] = '|'.join(placetypes)
		
		if price_range is not None:
			d['minprice'] = price_range
			d['maxprice'] = price_range
		
		if prefer_indoor is not None:
			d['keyword'] = 'indoor' if prefer_indoor else 'outdoor'

		location_data = json.loads(nearby_locs_from_type(d))
		
		return render_template("index.html", activities=Activity.query.order_by(Activity.activity_name).all())

@app.route('/api/v1/moodsearch', methods=['POST'])
def moodsearch():
	moods = [m[0] for m in Mood.query.with_entities(Mood.mood_name).all()]
	print(moods)
	if request.method == 'POST':
		data = request.get_json()
		vec = nlp(data['word'])
		mood_doc = [nlp(mood.lower()) for mood in moods]
		similarities = []
		for mood in mood_doc:
			similarities.append((vector_cosine_similarity(vec.vector, mood.vector), mood.text))
		print(jsonify({'payload': sorted(similarities, key=lambda x: x[0], reverse=True)[:5]}))
		return jsonify({'payload': sorted(similarities, key=lambda x: x[0], reverse=True)[:5]})
	else:
		return render_template('apologies.html')

@app.route('/api/v1/activity_mood_search', methods=['POST'])
def activity_mood_search():
	if request.method=='POST':
		data = request.get_json()
		# print(data)
		# print(data['word'])
		splitData = data['word'].split("<br>")
		result = []
		for i in range(len(splitData)):
			mood_query = Mood.query.filter_by(mood_name = splitData[i].upper()).with_entities(Mood.mood_id).all()
			activityIds = Mood_and_Activity.query.filter(Mood_and_Activity.mood_id.in_([i[0] for i in mood_query])).with_entities(Activity.activity_id).all()
			activity_list = Activity.query.filter(Activity.activity_id.in_([i[0] for i in activityIds])).with_entities(Activity.activity_id).all()
			result.extend([i[0] for i in activity_list])

		return jsonify({"result" : result})
	else:
		return render_template('apologies.html')

@app.route('/api/v1/filtersearch', methods=['POST'])
def filtersearch():
	if request.method == 'POST':
		data = request.get_json()
		d = {'key':API_KEY}
		if 'activities' in data.keys():
			d['type'] = '|'.join(getPlaces(data['activities']))

		if 'radius' in data.keys():
			d['radius'] = int(data['radius']) * 1000
		else:
			d['radius'] = 10000

		if 'price_range' in data.keys():
			d['minprice'] = d['maxprice'] = int(data['price_range'])-1
		
		if 'prefer_indoor' in data.keys():
			preference = int(data['prefer_indoor'])
			if preference==1:
				d['keyword'] = 'indoor'
			elif preference==2:
				d['keyword'] = 'outdoor'
		google_data = json.loads(nearby_locs_from_type(d))
		return jsonify(google_data)
	else:
		return render_template('apologies.html')


if __name__=='__main__':
	app.run(debug=True)