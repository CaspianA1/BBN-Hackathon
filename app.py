import os
from flask import Flask, render_template, request, redirect, session, flash
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
