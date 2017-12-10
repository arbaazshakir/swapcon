from app import db
import datetime
from hashlib import md5
from dateutil.relativedelta import relativedelta
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(64))
    #contacts = db.Column('contacts', db.PickleType(comparator=lambda *a: False)) #dictionary
    #tasks = db.Column('tasks', db.PickleType(comparator=lambda *a: False)) #dictionary
    created = db.Column(db.DateTime())
    contacts = db.relationship('Contact', backref='user', order_by="Contact.id", lazy='dynamic')
    tasks = db.relationship('Task', backref='user', order_by="Task.id",lazy='dynamic')
    profile_image_url = db.Column(db.String(400))
    primary_goal = db.Column(db.String(64)) #get_job, meet_people, find_mentor
    goals = db.relationship('Goal', backref='user', order_by="Goal.order", lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # python 3

    def get_info(self):
        return { "id" : self.id,
        "first_name" : self.first_name,
        "last_name" : self.last_name,
        "email" : self.email,
        "contacts" : self.contacts,
        "tasks" : self.tasks
        }
        
    def get_primary_goal_text(self):
        mapping = {
        'get_job' : 'Get a Job',
        'meet_people' : 'Meet People',
        'find_mentor' : 'Find a Mentor'
        }
        if self.primary_goal in mapping:
            return mapping[self.primary_goal]
        return self.primary_goal

    def get_active_subgoal_text_list(self):
        active_goals = [g for g in self.goals if g.is_active]


    def __repr__(self):
        return '<User %r>' % (self.email)

    default_image_url = "https://media.licdn.com/mpr/mpr/shrinknp_200_200/p/3/000/0f0/09c/143d675.jpg"
    def __init__(self, email, password, fn, ln, img_url=default_image_url, primary_goal='get_job'):
        self.email = email
        self.password = password
        self.first_name = fn
        self.last_name = ln
        self.contacts = {}
        self.tasks = {}
        self.created = datetime.datetime.now()
        if img_url==None:
            img_url=default_image_url
        self.profile_image_url = img_url
        self.primary_goal = primary_goal

#NOT A DATABASE CLASS (YET)
# class Task():
#     def __init__(self, task_type, due_date, body, is_done=False, contact_id=-1,
#         contact_name=""):
#         #task_type - string indicating one of the following:
#         ## Actual types are TBD
#         ## message, meeting, event, find_events, find_contacts, self_reminder

#         #due_date - datetime object for when task is due / happening
#         #body - string that describes the task
#         #is_active - True when before completion of task 

#         self.task_type = task_type
#         self.due_date = due_date
#         self.body = body
#         self.is_done = is_done
#         self.contact_id = contact_id # -1 indicates no contact associated with task
#         self.contact_name = contact_name # Empty str if no contact associated
#         self.task_id = -1 #no id assigned until added to user
#     def __repr__(self):
#         stat = "Todo"
#         if self.is_done:
#             stat= "Complete"
#         withContact = self.contact_name
#         message = "[{status}] {ttype} on {dateStr} {withC} <br> {body}"
#         dateStr = self.due_date.strftime("%b %d (%a) at %I%p")

#         if withContact:
#             return message.format(status=stat, ttype=self.task_type, 
#                 withC=withContract,dateStr=dateStr, body=self.body)
#         else:
#             return message.format(status=stat, ttype=self.task_type, 
#                 withC="",dateStr=dateStr, body=self.body)

#Below is what *would* be used for a formal database structure and much more efficient
#implementation. Instead, we're using python dictionaries for clarity and simplicity.

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column('id',db.Integer, primary_key=True)
    user_id = db.Column('user_id',db.Integer(), db.ForeignKey('users.id'))
    contact_id = db.Column('contact_id', db.Integer()) #NOT a foreign key bc can be null
    task_type = db.Column('task_type',db.String(140))
    due_date = db.Column('due_date',db.DateTime())
    is_done = db.Column('is_done',db.Boolean())
    body = db.Column('body',db.String(500))
    

    def __repr__(self):
        extra = "<a href='/tasks/{id}/edit'>Edit Task</a>".format(id=self.id)
        if self.contact_id != -1:
            extra += " | <a href='/contacts/{cid}'>View Contact</a>".format(cid=self.contact_id)
        
        return """ <p>Task - {task_type} <br>
        {body} <br>
        ---<br>
        Completed: {is_done} <br>
        Due Date: {due_date} <br></p> {extra}
        """.format(task_type=self.task_type, 
            body=self.body, 
            is_done=str(self.is_done), 
            due_date=str(self.due_date),
            extra=extra)

    def get_edit_url(self):
        return '/tasks/{id}/edit'.format(id=self.id)

    def __init__(self, task_type, due_date, body, user_id, is_done=False, contact_id=-1,
        contact_name=""):
        #task_type - string indicating one of the following:
        ## message, meeting, event, find_events, find_contacts, self_reminder

        #due_date - datetime object for when task is due / happening
        #body - string that describes the task
        #is_active - True when before completion of task 

        self.task_type = task_type
        self.due_date = due_date
        self.body = body
        self.user_id = user_id
        self.is_done = is_done
        self.contact_id = contact_id # -1 indicates no contact associated with task
        self.contact_name = contact_name # Empty str if no contact associated


#NOT A DATABASE CLASS (YET)
# class Contact():
#     def __init__(self, first_name, last_name, phone=None, email=None,
#       linkedin_url=None, notes="", events=[], idnum=-1):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.phone = phone
#         self.email = email
#         self.linkedin_url = linkedin_url
#         self.notes = notes
#         self.events = events
#         self.id = idnum

#     def __repr__(self):
#         return '<Contact :'+self.first_name+" "+self.last_name+">"

#     def get_url(self):
#         return '/contacts/'+str(self.id)

#     def full_name(self):
#         return self.first_name + " " + self.last_name

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(64))
    last_name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #who it belongs to
    email = db.Column(db.String(140))
    linkedin_url = db.Column(db.String(300))
    phone = db.Column(db.String(140))
    notes = db.Column(db.String(1000))
    #conversations = db.relationship('Conversation', backref='contact_id', lazy='dynamic')

    def __repr__(self):
        return "Contact - {name}".format(name=first_name+" "+last_name)

    def get_url(self):
        return '/contacts/'+str(self.id)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __init__(self, first_name, last_name, user_id, phone=None, email=None,
      linkedin_url=None, notes="", events=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.phone = phone
        self.email = email
        self.linkedin_url = linkedin_url
        self.notes = notes

class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    goal_type = db.Column(db.String(64)) # messages, new contacts, meetings, events
    goal_period = db.Column(db.String(64)) # day, week, month, completion
    goal_target = db.Column(db.Integer)
    current_count = db.Column(db.Integer) #current count for period
    next_period_start = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean) #shows up on profile or not
    order = db.Column(db.Integer) #order preference to be displayed in, HIGHER is on TOP

    def edit_url(self):
        return "/goals/{id}/edit".format(id=self.id)

    def __init__(self, user_id, goal_type, goal_period, goal_target, current_count=0, 
        next_period_start=None, is_active=True, order=None):
        self.user_id = user_id
        self.goal_type = goal_type
        self.goal_period = goal_period
        self.goal_target = goal_target
        self.current_count = current_count
        if next_period_start == None and goal_period != 'completion':
            now = datetime.datetime.now()
            if goal_period == 'day':
                td = datetime.timedelta(days=1)
            elif goal_period == 'week':
                td = datetime.timedelta(days=7)
            else: # goal_period == 'month':
                td = relativedelta(months=1)
            self.next_period_start=now+td
        self.is_active = is_active
        if order == None:
            order = self.id
        self.order=order

    def __repr__(self):
        output = ""
        dateStr = self.next_period_start.strftime("%b %d (%a) at %I%p")
        if self.goal_period == 'completion':
            periodStr = 'total (to completion)'
        else:
            periodStr = 'per '+self.goal_period

        if self.is_active:
            activeStr = '[ACTIVE: {c} Completed]'.format(c=self.current_count)
        else:
            activeStr = '[DONE]'

        if 'message' in self.goal_type:
            output = "Message {target} people by {date} {period} {active}".format(
                target=self.goal_target,
                date=dateStr,
                period=periodStr,
                active=activeStr)

        elif 'contact' in self.goal_type:
            output = "Make {target} contacts by {date} {period} {active}".format(
                target=self.goal_target,
                date=dateStr,
                period=periodStr,
                active=activeStr)
        elif 'meet' in self.goal_type:
            output = "Go to {target} meetings by {date} {period} {active}".format(
                target=self.goal_target,
                date=dateStr,
                period=periodStr,
                active=activeStr)
        elif 'event' in self.goal_type :
            output = "Go to {target} events by {date} {period} {active}".format(
                target=self.goal_target,
                date=dateStr,
                period=periodStr,
                active=activeStr)
        else:
            output = "{goal}  - {current}/{target} - Do by {date} {period}".format(
                goal=self.goal_type,
                current=self.current_count,
                target=self.goal_target,
                date=dateStr,
                period=periodStr,
                active=activeStr)

        return output