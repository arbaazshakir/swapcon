import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import *
from .models import User, Contact, Task
import sqlalchemy
from time import sleep

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
@login_required
def index():
    print(current_user.first_name)
    user = current_user
    tasks = user.get_info()['tasks']
    active_tasks = []
    for task in tasks.values():
      if not task.is_done:
        active_tasks.append(task)

    return render_template('index.html',
                           title='Home',
                           user=user,
                           active_tasks=active_tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
          if user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
          else:
            flash("Wrong password")
        else:
          flash("User does not exist")
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        existingUser = User.query.filter_by(email=form.email.data).first()
        if not existingUser:
          user = User(form.email.data,
                      form.password.data,
                      form.first_name.data,
                      form.last_name.data)
          db.session.add(user)
          db.session.commit()
          flash('Thanks for registering')
          return redirect(url_for('login'))
        else:
          flask('User with that email already exists')
    return render_template('register.html', form=form)\

@app.route('/contacts', methods=['GET'])
@login_required
def contacts():
  if current_user.contacts:
    keys = sorted(current_user.contacts.keys(), reverse=True)
    result = [current_user.contacts[key] for key in keys]
  else:
    result = []
  return render_template('contacts.html', user=current_user, contacts=result)

@app.route('/add_contact', methods=['GET', 'POST'])
@login_required
def add_contact():
  form = ContactForm()
  if form.validate_on_submit():
    print(form)
    newContact = Contact(form.first_name.data,
                      form.last_name.data,
                      form.phone.data,
                      form.email.data,
                      form.linkedin_url.data,
                      notes=form.notes.data)
    #SqlAlchemy requires writing a new object to update a pickled object!
    #-->Can't Modify data within to trigger an update
    ids = list(current_user.contacts.keys())+[-1]
    max_id = max(ids)
    tempContacts = dict(current_user.contacts)
    newContact.id = max_id+1
    tempContacts[max_id+1] = newContact
    current_user.contacts = tempContacts
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('contacts'))
  return render_template('add_contact.html',
                          user=current_user, 
                          form=form)

@app.route('/contacts/<contact_id>')
@login_required
def get_contact(contact_id):
  if int(contact_id) in current_user.contacts:
    return render_template('contact.html',
                          title='View Contact',
                          user=current_user,
                          contact=current_user.contacts[int(contact_id)])
  flash("Invalid contact!")
  return "Invalid contact!"

@app.route('/contacts/<contact_id>/edit', methods=['GET','POST'])
@login_required
def edit_contact(contact_id):
  c = current_user.contacts[int(contact_id)]
  form = EditContactForm()
  form.first_name.data = c.first_name
  form.last_name.data = c.last_name
  form.phone.data = c.phone
  form.email.data = c.email
  form.linkedin_url.data = c.linkedin_url
  form.notes.data = c.notes
  if request.method == 'POST' and form.validate():
    tempContacts = current_user.contacts.copy()
    updateC = Contact(form.first_name.data, form.last_name.data, phone=form.phone.data,
      email=form.email.data, linkedin_url=form.linkedin_url.data, notes=form.notes.data,
      events=c.events, idnum=int(contact_id))
    
    current_user.contacts = {}
    db.session.execute(sqlalchemy.update(User).where(User.id == current_user.id).values(contacts={}))
    db.session.commit()
    tempContacts[int(contact_id)] = updateC
    current_user.contacts = tempContacts
    db.session.commit()
    return redirect(url_for('contacts'))
  return render_template('edit_contact.html',
                          title='Edit Contact',
                          user=current_user,
                          contact=c,
                          form=form)

@app.route('/tasks')
@login_required
def tasks():
  keys = sorted(current_user.tasks.keys(), reverse=True)
  result = [current_user.tasks[key] for key in keys]
  return render_template('tasks.html', user=current_user, tasks=result)

@app.route('/add_task', methods=['GET','POST'])
@login_required
def add_task():
  contact_list = [(-1,"None / NA")]
  for key in current_user.contacts.keys():
    contact = current_user.contacts[key]
    option_str = "{id} - {name}".format(id=str(key), name=contact.full_name())
    contact_list.append((int(key), option_str))
  form=TaskForm()
  form.relevant_contact.choices=contact_list

  if request.method == 'POST' and form.validate():
    date = form.due_date.data
    hour = form.due_time_hour.data + 12*form.due_time_ampm.data
    minute = form.due_time_minute.data
    due_date = datetime.datetime(date.year,date.month,date.day, hour, minute)

    task_type = form.task_type.data
    body = form.body.data
    rel_contact_id = form.relevant_contact.data
    rel_contact_name = ""
    if rel_contact_id != -1:
      rel_contact_name = current_user.contacts[rel_contact_id].full_name()

    newTask = Task(task_type, due_date, body, is_done=False, 
      contact_id=rel_contact_id, contact_name=rel_contact_name)
    
    ids = list(current_user.tasks.keys())
    ids.append(-1) #in case no tasks exist
    task_id = max(ids)+1
    newTask.task_id = task_id
    tempDict = current_user.tasks.copy()
    tempDict[task_id] = newTask
    
    current_user.tasks = tempDict
    db.session.commit()
    
    flash("Task added successfully")
    return redirect(url_for('index'))
  return render_template('add_task.html',
                        title='Add Task',
                        user=current_user,
                        form=form) 
