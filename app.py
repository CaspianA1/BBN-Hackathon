import os
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from db_construction import Activity, Placetype, Comment
import requests, json, datetime, nltk, ssl, spacy, en_core_web_md, math

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


nlp = en_core_web_md.load()

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackathon2021.db'
db = SQLAlchemy(app)
app.secret_key = 'somethingsecret'
app.config["SESSION_TYPE"] = 'filesystem'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method =='GET':# Activity.query.order_by(Activity.activity_name).all()
        return render_template("index.html", activities=Activity.query.order_by(Activity.activity_name).all(), results=False)
    else:
        #checklist will be all the filtered activites
        checkList = []
        for activity_check in request.form.keys():
            if 'typeCheck' in activity_check and request.form.get(activity_check) == 'on':
                checkList.append(activity_check.split('@')[1].strip())

        return render_template("index.html", activities=Activity.query.order_by(Activity.activity_name).all())

@app.route('/api/v1/moodsearch', methods=['POST'])
def moodsearch():
    moods = ['happy', 'sad', 'tired', 'angry', 'excited']
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        vec = nlp(data['word'])
        mood_doc = nlp(' '.join(moods))
        similarities = []
        for mood in mood_doc:
            similarities.append((vector_cosine_similarity(vec.vector, mood.vector), mood.text))
            
        return jsonify({'payload': sorted(similarities, key=lambda x: x[0], reverse=True)[:5]})
    else:
        return render_template('apologies.html')


def vector_cosine_similarity(vec1,vec2):
    #Assume vec1 and vec2 have the same size 
    dot_product = 0
    vec1_sum = 0
    vec2_sum = 0
    for i, v_1 in enumerate(vec1):
        dot_product += v_1 * vec2[i]
        vec1_sum += v_1**2
        vec2_sum += vec2[i]**2

    return dot_product/(math.sqrt(vec1_sum)*math.sqrt(vec2_sum))


"""
input: checkList --> a list of the items checked
output: a list of the associated Placetype Ids
"""
def getPlaces(checkList):
    finalString = ""
    listOfPlaces = set()
    for i in range(len(checkList)):
        activityList = Activity.query.filter_by(activity_name = checkList[i]).first()
        finalString = finalString + activityList
        listOfPlaces.union(set(activityList.split(' ')))
    return listOfPlaces

if __name__=='__main__':
    app.run(debug=True)
