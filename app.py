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



class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String, nullable=True, default="Anonymous")
    message = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Comment {self.comment_id} Written by {self.author_name} with message {self.message}"


@app.route('/')
def index():
    return render_template("index.html")




