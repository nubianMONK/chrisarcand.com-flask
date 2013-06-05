from flask.ext.wtf import Form, validators
from wtforms import TextField, TextAreaField, RadioField

class ContactForm(Form):
    name = TextField('Name', [validators.DataRequired()])
    email = TextField('Email Address', [validators.DataRequired(), validators.Email()])
    body = TextAreaField('Message', [validators.DataRequired()])