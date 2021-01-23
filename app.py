import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from db_construction import Activity, Placetype, Comment
import requests, json, datetime

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackathon2021.db'
db = SQLAlchemy(app)
app.secret_key = 'somethingsecret'
app.config["SESSION_TYPE"] = 'filesystem'


@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")

"""
input: checkList --> a list of the items checked
output: a list of the associated Placetype Ids
"""
def getPlaces(checkList):
    finalString = ""
    listOfPlaces = []
    for i in range(len(checkList)):
        activityList = Activity.query.filter_by(activity_name = checkList[i])
        finalString = finalString + activityList
        for j in activityList.split(' '):
            if(listOfPlaces.find(j)==-1): 
                listOfPlaces.append(j)
    return listOfPlaces