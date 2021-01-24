import os
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from db_construction import Activity, Placetype, Comment, Action, Mood
from helper import vector_cosine_similarity, getPlaces
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





if __name__=='__main__':
    app.run(debug=True)
