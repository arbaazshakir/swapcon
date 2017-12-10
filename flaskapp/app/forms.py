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
    linkedin_url = StringField('linkedin_url', validators=[Optional(), URL(message=url_message)])
    #Todo add note with TextAreaField!!!

class TaskForm(Form):
    due_date = DateField('due_date', validators=[DataRequired()], format='%Y-%m-%d', default=datetime.datetime.today())
    due_times_hour = [(0, '12:00'),(1, '1:00'), (2, '2:00'), (3, '3:00'), (4, '4:00'), (5, '5:00'), (6, '6:00'), (
7, '7:00'), (8, '8:00'), (9, '9:00'), (10, '10:00'), (11, '11:00')]
    due_time_hour = SelectField('due_time_hour', validators=[DataRequired()], choices=due_times_hour)
    due_time_ampm = SelectField('due_time_ampm', validators=[DataRequired()], choices=[(0,'AM'),(1,'PM')]) 
    due_times_minute = [(x, str(x)) for x in range(0,60,5)]
    due_time_minute = SelectField('due_time_minute', validators=[DataRequired()], choices=due_times_minute)
    task_types = ['message', 'meeting', 'event', 'find_events', 'find_contacts', 'self_reminder']
    task_choices = [(x, x) for x in task_types]
    task_type = SelectField('task_type',choices=task_choices, validators=[DataRequired()])
    body = TextAreaField("Notes", validators=[DataRequired()])
    relevant_contact = SelectField('contact', choices=[(-1, "None / NA")], validators=[DataRequired()])
