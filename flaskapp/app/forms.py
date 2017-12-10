from wtforms import *
from flask_wtf import Form
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional, URL
import datetime

email_message = "Please enter a valid email."
url_message = "Please enter a valid url"

class LoginForm(Form):
    email = StringField('email', validators=[DataRequired(), Email(message=email_message)])
    password = PasswordField('password', validators=[DataRequired()])

class RegistrationForm(Form):
    email = StringField('Email Address', [Email(message=email_message)])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    accept_tos = BooleanField('I accept the TOS', [DataRequired()])

class ContactForm(Form):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional(), Length(min=7, max=20)])
    email = StringField('email', validators=[Optional(), Email(message=email_message)])
    linkedin_url = StringField('linkedin_url', validators=[Optional()])
    notes = TextAreaField("Notes")

class EditContactForm(Form):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional()])
    email = StringField('email', validators=[Optional(), Email(message=email_message)])
    linkedin_url = StringField('linkedin_url', validators=[Optional(), URL(message=url_message)])
    notes = TextAreaField("Notes")

class TaskForm(Form):
    due_date = DateField('due_date', format='%Y-%m-%d', default=datetime.datetime.today())
    due_times_hour = [(0, '12:00'),(1, '1:00'), (2, '2:00'), (3, '3:00'), (4, '4:00'), (5, '5:00'), (6, '6:00'), (
7, '7:00'), (8, '8:00'), (9, '9:00'), (10, '10:00'), (11, '11:00')]

    due_time_hour = SelectField('due_time_hour',coerce=int, choices=due_times_hour, default=datetime.datetime.now().hour%12)
    due_time_ampm = SelectField('due_time_ampm',coerce=int, choices=[(0,'AM'),(1,'PM')], default=int(datetime.datetime.now().hour>12)) 
    due_times_minute = [(x, str(x)) for x in range(0,60,5)]

    due_time_minute = SelectField('due_time_minute', coerce=int, choices=due_times_minute,default=0)
    task_types = ['message', 'meeting', 'event', 'find_events', 'find_contacts', 'self_reminder']
    task_choices = [(x, x) for x in task_types]
    task_type = SelectField('task_type', coerce=str, choices=task_choices, default='message')
    body = TextAreaField("Notes")
    relevant_contact = SelectField('contact', coerce=int, choices=[(-1, "None / NA")], validators=[Optional()])
    is_done = BooleanField('is_done')

