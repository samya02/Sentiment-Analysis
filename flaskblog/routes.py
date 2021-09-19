from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, HashtagtForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.sentiment import get_tweets, tweet_to_data_frame, cleantext, getPolarity, getSubjectivity, getAnalysis, positivetweets, negativetweets, neutraltweets
import re
import collections

@app.route('/')
@app.route('/home/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/contact/')
def contact():
    return render_template("contact.html")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html') 

@app.route('/meditate/')
def mediate():
    return render_template("meditate.html")

@app.route('/tweet_analysis', methods=['GET', 'POST'])
def tweet_analysis():
    form = HashtagtForm()
    if form.validate_on_submit():
        hash1 = request.form['hashtag']
        hash = request.form['hashtag'] + ' -filter:retweets'
        alltweets = get_tweets(hash)
        data = tweet_to_data_frame(alltweets)
        data['Tweets'] = data['Tweets'].apply(cleantext)
        data['Subjectivity'] = data['Tweets'].apply(getSubjectivity)
        data['Polarity'] = data['Tweets'].apply(getPolarity)
        data['Analysis'] = data['Polarity'].apply(getAnalysis)
        pos = positivetweets(data)
        neg = negativetweets(data)
        neu = neutraltweets(data)
        division = [pos, neg, neu]
        words = []
        for tweet in data['Tweets']:
            wordList = re.sub("[^\w]", " ",  tweet).split()
            words = words + wordList
        
        words = []
        for tweet in data['Tweets']:
            wordList = re.sub("[^\w]", " ",  tweet).split()
            words = words + wordList
        stopwords = ['amp','I','The', 'us','re','it','to','the','and','you','a','of', 'for', 'thus']
        filtered_words = [word for word in words if word not in stopwords]
        counted_words = collections.Counter(filtered_words)

        common_words = []
        counts = []
        for letter, count in counted_words.most_common(10):
            common_words.append(letter)
            counts.append(count)
        return render_template('result_analysis.html', hash1=hash1, data = data, pos=pos, neg=neg, neu=neu, division=division, common_words=common_words, counts=counts)
    return render_template('tweet_analysis.html', form=form)

@app.route('/result_analysis')
def result_analysis():
    return render_template('result_analysis.html')