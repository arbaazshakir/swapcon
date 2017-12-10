from app import db
from datetime import datetime

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
        self.created = datetime.now()

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