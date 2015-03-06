from flask.ext.wtf import Form

from wtforms import TextField, BooleanField, SubmitField, TextAreaField, ValidationError, PasswordField, validators
from wtforms.validators import Required
from models import db, User

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter a name.")])
  email = TextField("Email",  [validators.Required("Please enter an email address."), validators.Email("Please enter an email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

class SignupForm(Form):
  nickname = TextField("Nickname",  [validators.Required("Please enter a nickname")])
  email = TextField("Email",  [validators.Required("Please enter an email address."), validators.Email("Please enter an email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False

    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email has already been taken")
      return False
    else:
      return True

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter an email address."), validators.Email("Please enter an email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False

    user = User.query.filter_by(email = self.email.data).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail and or password")
      return False
