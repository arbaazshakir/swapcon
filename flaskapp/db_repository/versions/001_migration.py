from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
contact = Table('contact', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('first_name', VARCHAR(length=64)),
    Column('last_name', VARCHAR(length=64)),
    Column('user_id', INTEGER),
    Column('email', VARCHAR(length=140)),
    Column('linkedin_url', VARCHAR(length=300)),
    Column('phone', VARCHAR(length=140)),
    Column('notes', VARCHAR(length=1000)),
)

task = Table('task', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('contact_id', INTEGER),
    Column('task_type', VARCHAR(length=140)),
    Column('due_date', DATETIME),
    Column('is_done', BOOLEAN),
    Column('body', VARCHAR(length=500)),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('first_name', VARCHAR(length=64)),
    Column('last_name', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('password', VARCHAR(length=64)),
    Column('created', DATETIME),
)

contacts = Table('contacts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=64)),
    Column('user_id', Integer),
    Column('email', String(length=140)),
    Column('linkedin_url', String(length=300)),
    Column('phone', String(length=140)),
    Column('notes', String(length=1000)),
)

tasks = Table('tasks', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('contact_id', Integer),
    Column('task_type', String(length=140)),
    Column('due_date', DateTime),
    Column('is_done', Boolean),
    Column('body', String(length=500)),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=64)),
    Column('created', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['contact'].drop()
    pre_meta.tables['task'].drop()
    pre_meta.tables['user'].drop()
    post_meta.tables['contacts'].create()
    post_meta.tables['tasks'].create()
    post_meta.tables['users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['contact'].create()
    pre_meta.tables['task'].create()
    pre_meta.tables['user'].create()
    post_meta.tables['contacts'].drop()
    post_meta.tables['tasks'].drop()
    post_meta.tables['users'].drop()
