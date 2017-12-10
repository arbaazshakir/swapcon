from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(64))
    contacts = db.Column(db.PickleType) #dictionary
    tasks = db.Column(db.PickleType) #dictionary

    #Below is what we'd use if we were using a formal db structure.
    #Currently using pickled python dictionaries for simplicity.
    # contacts = db.relationship('Contact', backref='user_id', lazy='dynamic')
    # tasks = db.relationship('Task', backref='user_id', lazy='dynamic')

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
        
    def __repr__(self):
        return '<User %r>' % (self.email)


    def __init__(self, email, password, fn, ln):
        self.email = email
        self.password = password
        self.first_name = fn
        self.last_name = ln
        self.contacts = {}
        self.tasks = {}

#NOT A DATABASE CLASS (YET)
class Task():
    def __init__(self, task_type, due_date, body, is_done=False, contact_id=-1,
        contact_name=""):
        #task_type - string indicating one of the following:
        ## Actual types are TBD
        ## message, meeting, event, find_events, find_contacts, self_reminder

        #due_date - datetime object for when task is due / happening
        #body - string that describes the task
        #is_active - True when before completion of task 

        self.task_type = task_type
        self.due_date = due_date
        self.body = body
        self.is_done = is_done
        self.contact_id = contact_id # -1 indicates no contact associated with task
        self.contact_name = contact_name # Empty str if no contact associated
        self.task_id = -1 #no id assigned until added to user
    def __repr__(self):
        stat = "Todo"
        if self.is_done:
            stat= "Complete"
        withContact = self.contact_name
        message = "[{status}] {ttype} on {dateStr} {withC} <br> {body}"
        dateStr = self.due_date.strftime("%b %d (%a) at %I%p")

        if withContact:
            return message.format(status=stat, ttype=self.task_type, 
                withC=withContract,dateStr=dateStr, body=self.body)
        else:
            return message.format(status=stat, ttype=self.task_type, 
                withC="",dateStr=dateStr, body=self.body)

#NOT A DATABASE CLASS (YET)
class Contact():
    def __init__(self, first_name, last_name, phone=None, email=None,
      linkedin_url=None, notes="", events=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.linkedin_url = linkedin_url
        self.notes = notes
        self.events = events
        self.id = -1

    def __repr__(self):
        return '<Contact :'+self.first_name+" "+self.last_name+">"

    def get_url(self):
        return '/contacts/'+str(self.id)

    def full_name(self):
        return self.first_name + " " + self.last_name

#Below is what *would* be used for a formal database structure and much more efficient
#implementation. Instead, we're using python dictionaries for clarity and simplicity.

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     task_type = db.Column(db.String(140))
#     due_date = db.Column(db.DateTime)
#     is_done = db.Column(db.Boolean)
#     body = db.Column(db.String(500))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return """ Task - {task_type}
#         {body}
#         ---
#         Completed: {is_done}
#         Due Date: {due_date}
#         """.format(task_type=task_type, 
#             body=body, 
#             is_done=is_done, 
#             due_date=due_date)

# class Contact(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(64))
#     last_name = db.Column(db.String(64))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     email = db.Column(db.String(140))
#     linkedin_url = db.Column(db.String(140))
#     phone = db.Column(db.String(140))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     conversations = db.relationship('Conversation', backref='contact_id', lazy='dynamic')

#     def __repr__(self):
#         return "Contact - {name}".format(name=first_name+" "+last_name)


# class Conversation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     convo_type = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime)
#     method = db.Column(db.String(140))
#     contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     body = db.Column(db.String(5000))

#     def __repr__(self):
#         return """ Convo - {convo_type}
#         {body}
#         ---
#         Method: {method}
#         Date: {timestamp}
#         """.format(task_type=task_type, 
#             body=body, 
#             method=method, 
#             timestamp=timestamp)