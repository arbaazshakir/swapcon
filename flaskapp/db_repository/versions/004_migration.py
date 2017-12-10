from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
contact = Table('contact', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('first_name', VARCHAR(length=64)),
    Column('last_name', VARCHAR(length=64)),
    Column('email', VARCHAR(length=140)),
    Column('linkedin_url', VARCHAR(length=140)),
    Column('phone', VARCHAR(length=140)),
    Column('user_id', INTEGER),
)

conversation = Table('conversation', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('convo_type', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('method', VARCHAR(length=140)),
    Column('contact_id', INTEGER),
    Column('user_id', INTEGER),
    Column('body', VARCHAR(length=5000)),
)

task = Table('task', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('task_type', VARCHAR(length=140)),
    Column('due_date', DATETIME),
    Column('is_done', BOOLEAN),
    Column('body', VARCHAR(length=500)),
    Column('user_id', INTEGER),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=64)),
    Column('contacts', PickleType),
    Column('tasks', PickleType),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['contact'].drop()
    pre_meta.tables['conversation'].drop()
    pre_meta.tables['task'].drop()
    post_meta.tables['user'].columns['contacts'].create()
    post_meta.tables['user'].columns['tasks'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['contact'].create()
    pre_meta.tables['conversation'].create()
    pre_meta.tables['task'].create()
    post_meta.tables['user'].columns['contacts'].drop()
    post_meta.tables['user'].columns['tasks'].drop()
