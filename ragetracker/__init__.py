from flask import Flask
from flaskext.markdown import Markdown
import os

app = Flask(__name__)
Markdown(app)

app.secret_key = 'development key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'contact@example.com'
app.config["MAIL_PASSWORD"] = 'your-password'

from routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

from models import db


db.init_app(app)

with app.app_context():
  if not os.path.exists('app.db'):
    db.create_all()


import ragetracker.routes
