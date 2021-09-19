from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import tweepy
import numpy as np
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

consumer_key    = 'pBCO7GgCXz5P4CwJiC1A9ulRR'
consumer_secret = 'HEivIT6n18EJ7VkkiJOrLxR0DnArM1gcPDURdYXDB2N8gwHlbw'
access_token    = '3104782429-oorTzK3fWhJW7MknotNTPveZzlvCj64ZSCgpuXp' 
access_secret   = 'gvJ9uXoo13L1UNhsmzhdMTifEQ3rQhQcl6jr5PcxwKdE2'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

from flaskblog import routes 