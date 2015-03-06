from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  nickname = db.Column(db.String(100))
  statsBlob = db.Column(db.Binary())
  email = db.Column(db.String(120), unique=True)
  killCount = db.Column(db.Integer, default=0)
  pwdhash = db.Column(db.String(54))

  def __init__(self, nickname, email, password):
    self.nickname = nickname.title()
    self.email = email.lower()
    self.set_password(password)

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class BossKill(db.Model):
  __tablename__ = 'bosskills'
  uid = db.Column(db.Integer, primary_key = True)
  boss_id = db.Column(db.Integer)
  user_id = db.Column(db.Integer)
  defeatedDate = db.Column(db.DateTime)

  def __init__(self, boss_id, user_id, defeatedDate):
    self.boss_id = boss_id
    self.user_id = user_id
    self.defeatedDate = defeatedDate
