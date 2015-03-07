from ragetracker import app
from flask import render_template, request, flash, session, url_for, redirect
from forms import ContactForm, SignupForm, SigninForm
from flask.ext.mail import Message, Mail
from models import db, User, BossKill
from datetime import datetime
from darksouls import DarkSouls

mail = Mail()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.nickname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('profile'))

  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).first()
  session['nickname'] = user.nickname
  session['killCount'] = user.killCount

  souls = DarkSouls()
  session['currentEnemy'] = souls.getBoss(user.killCount)

  if user is None:
    return redirect(url_for('signin'))
  else:
    stats = BossKill.query.filter_by(user_id = user.uid).all()
    return render_template('profile.html', stats=stats)

@app.route('/profile/<int:id>')
def userProfile(id):
  user = User.query.filter_by(uid = id).first()

  if user:
    session['nickname'] = user.nickname
    session['killCount'] = user.killCount

    souls = DarkSouls()
    session['currentEnemy'] = souls.getBoss(user.killCount)
    stats = BossKill.query.filter_by(user_id = user.uid).all()
    return render_template('user_profile.html', stats=stats)
  else:
    return render_template('error/user_profile.html')

@app.route('/dashboard')
def getDashboard():
  return render_template('error/not_implemented.html')

@app.route('/defeated')
def defeated():
  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).first()
  kCount = user.killCount + 1
  user.killCount = kCount

  bossKill = BossKill(kCount, user.uid, datetime.utcnow())
  db.session.add(bossKill)
  db.session.commit()

  return redirect(url_for('profile'))

@app.route('/reset')
def reset():
  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).first()
  user.killCount = 0
  db.session.commit()

  return redirect(url_for('profile'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'email' in session:
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))

  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('signin'))

  session.pop('email', None)
  return redirect(url_for('home'))
