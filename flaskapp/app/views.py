import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import *
from .models import User, Contact, Task, Goal
import sqlalchemy
from time import sleep

def earliest_x_tasks(x, tasks):
  #e.g. x=5, gets the first five
  tasksByDate = sorted(tasks, key=lambda task: task.due_date.timestamp())
  return tasksByDate[:min(len(tasks),x)]

def last_x_tasks(x, tasks):
  tasksByDate = sorted(tasks, key=lambda task: task.due_date.timestamp(), reverse=True)
  return tasksByDate[:min(len(tasks),x)]

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
@login_required
def index():
    print(current_user.first_name)
    user = current_user
    tasks = user.tasks
    active_tasks = []
    inactive_tasks = []
    for task in tasks:
      if not task.is_done:
        active_tasks.append(task)
      else:
        inactive_tasks.append(task)
    active_tasks = earliest_x_tasks(5, active_tasks)
    inactive_tasks = last_x_tasks(5, inactive_tasks)

    return render_template('index.html',
                           title='Home',
                           user=user,
                           active_tasks=active_tasks,
                           num_tasks=len(active_tasks),
                           inactive_tasks=inactive_tasks,
                           num_inactive_tasks=len(inactive_tasks),
                           goals=list(current_user.goals))

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
                      form.last_name.data,
                      form.profile_image_url.data,
                      form.primary_goal.data)
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
    result = list(current_user.contacts)
  else:
    result = []
  return render_template('contacts.html', user=current_user, contacts=result,
    num_contacts=len(result))

@app.route('/add_contact', methods=['GET', 'POST'])
@login_required
def add_contact():
  form = ContactForm()
  if form.validate_on_submit():
    print(form)
    newContact = Contact(form.first_name.data,
                      form.last_name.data,
                      current_user.id,
                      form.phone.data,
                      form.email.data,
                      form.linkedin_url.data,
                      form.notes.data)
    db.session.add(newContact)
    db.session.commit()
    return redirect(url_for('contacts'))
  return render_template('add_contact.html',
                          user=current_user, 
                          form=form)

@app.route('/contacts/<contact_id>')
@login_required
def get_contact(contact_id):
  c = Contact.query.get(int(contact_id))
  tasks_with_c = Task.query.filter_by(contact_id=int(contact_id)).all()
  num_tasks = len(tasks_with_c)
  if c:
    return render_template('contact.html',
                          title='View Contact',
                          user=current_user,
                          contact=c,
                          tasks=tasks_with_c,
                          num_tasks=num_tasks)
  flash("Invalid contact!")
  return "Invalid contact!"

@app.route('/contacts/<contact_id>/edit', methods=['GET','POST'])
@login_required
def edit_contact(contact_id):
  c = Contact.query.get(int(contact_id))
  form = EditContactForm()
  if request.method == 'POST' and form.validate():
    print(form.first_name.data)
    print(form.notes.data)
    c.first_name = form.first_name.data
    c.last_name = form.last_name.data
    c.phone = form.phone.data
    c.email = form.email.data
    c.linkedin_url = form.linkedin_url.data
    c.notes = form.notes.data
    db.session.commit()
    return redirect(url_for('contacts'))
  form.first_name.data = c.first_name
  form.last_name.data = c.last_name
  form.phone.data = c.phone
  form.email.data = c.email
  form.linkedin_url.data = c.linkedin_url
  form.notes.data = c.notes
  return render_template('edit_contact.html',
                          title='Edit Contact',
                          user=current_user,
                          contact=c,
                          form=form)

@app.route('/tasks')
@login_required
def tasks():
  if current_user.tasks:
    result = list(current_user.tasks)
  else:
    result = []
  return render_template('tasks.html', user=current_user, tasks=result,
    num_tasks=len(result))



@app.route('/add_task', methods=['GET','POST'])
@login_required
def add_task():
  contact_list = [(-1,"None / NA")]
  for contact in current_user.contacts:
    option_str = "{name}".format(name=contact.full_name())
    contact_list.append((int(contact.id), option_str))
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
      rel_contact_name = Contact.query.get(int(rel_contact_id)).full_name()

    is_done = form.is_done.data

    newTask = Task(task_type, due_date, body, current_user.id, is_done=is_done, 
      contact_id=rel_contact_id, contact_name=rel_contact_name)
    
    db.session.add(newTask)
    db.session.commit()
    
    flash("Task added successfully")
    return redirect(url_for('tasks'))
  return render_template('add_task.html',
                        title='Add Task',
                        user=current_user,
                        form=form) 

@app.route('/tasks/<task_id>')
@login_required
def view_task(task_id):
  return redirect(url_for('tasks'))


@app.route('/tasks/<task_id>/edit', methods=['GET','POST'])
@login_required
def edit_task(task_id):
  task = Task.query.get(int(task_id))
  contact_list = [(-1,"None / NA")]
  for contact in current_user.contacts:
    option_str = "{name}".format(name=contact.full_name())
    contact_list.append((int(contact.id), option_str))
  form = TaskForm()
  form.relevant_contact.choices=contact_list
  if request.method == 'POST' and form.validate():
    date = form.due_date.data
    hour = form.due_time_hour.data + 12*form.due_time_ampm.data
    minute = form.due_time_minute.data
    task.due_date = datetime.datetime(date.year,date.month,date.day, hour, minute)

    task.task_type = form.task_type.data
    task.body = form.body.data
    task.contact_id = int(form.relevant_contact.data)
    if task.contact_id != -1:
      task.contact_name = Contact.query.get(task.contact_id).full_name()

    #see if action is being completed
    if not task.is_done and form.is_done.data:
      #track update into goals if applicable
      goals = []
      for goal in current_user.goals:
        if goal.is_active and (task.task_type in goal.goal_type):
          #in because e.g. task_type can be 'meeting' and goal_type can be 'meetings'
          goal.current_count += 1

    task.is_done = form.is_done.data
    db.session.commit()
    flash("Task updated successfully")
    return redirect(url_for('tasks'))
  form.due_date.data = task.due_date
  form.task_type.data = task.task_type
  form.body.data = task.body
  form.relevant_contact.data = task.contact_id
  form.is_done.data = task.is_done
  return render_template('edit_task.html',
                        title='Edit Task',
                        user=current_user,
                        form=form)

@app.route('/profile')
@login_required
def profile():
  return render_template('profile.html',
                        title='Profile',
                        user=current_user,
                        goals=list(current_user.goals))

@app.route('/profile/edit', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate():
      current_user.first_name = form.first_name.data
      current_user.last_name = form.last_name.data
      current_user.profile_image_url =form.profile_image_url.data
      current_user.primary_goal = form.primary_goal.data
      db.session.commit()
      flash('Profile Successfully Updated!')
      return redirect(url_for('profile'))

    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.profile_image_url.data = current_user.profile_image_url
    key_choices = [x[0] for x in form.primary_goal.choices]
    if current_user.primary_goal in key_choices:
      form.primary_goal.data = current_user.primary_goal
    return render_template('edit_profile.html',
                          title='Edit Profile',
                          user=current_user,
                          form=form)

@app.route('/goals/')
@login_required
def goals():
  return render_template('goals.html',
                        title='View Goals',
                        user=current_user,
                        goals=list(current_user.goals))

@app.route('/goals/add', methods=['GET','POST'])
@login_required
def add_goal():
  form = GoalForm()
  if request.method == 'POST' and form.validate():
    g = Goal(current_user.id,
            form.goal_type.data,
            form.goal_period.data,
            form.goal_target.data,
            form.current_count.data)
    db.session.add(g)
    db.session.commit()
    return redirect(url_for('index'))
  return render_template('add_goal.html',
                        title='Add Goal',
                        user=current_user,
                        form=form)

@app.route('/goals/<goal_id>/edit', methods=['GET','POST'])
@login_required
def edit_goal(goal_id):
  g = Goal.query.get(int(goal_id))
  form = EditGoalForm()
  if request.method == 'POST' and form.validate():
    g.goal_type = form.goal_type.data
    g.goal_period = form.goal_period.data
    g.goal_target = form.goal_target.data
    g.current_count = form.current_count.data
    g.is_active = (not form.remove.data)
    db.session.add(g)
    db.session.commit()
    return redirect(url_for('index'))
  form.goal_type.data = g.goal_type
  form.goal_period.data = g.goal_period
  form.goal_target.data = g.goal_target
  form.current_count.data = g.current_count
  return render_template('edit_goal.html',
                        title="Edit Goal",
                        user=current_user,
                        form=form)
