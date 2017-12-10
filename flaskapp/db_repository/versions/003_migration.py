from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
)

contact = Table('contact', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=64)),
    Column('email', String(length=140)),
    Column('linkedin_url', String(length=140)),
    Column('phone', String(length=140)),
    Column('user_id', Integer),
)

conversation = Table('conversation', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('convo_type', String(length=140)),
    Column('timestamp', DateTime),
    Column('method', String(length=140)),
    Column('contact_id', Integer),
    Column('user_id', Integer),
    Column('body', String(length=5000)),
)

task = Table('task', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('task_type', String(length=140)),
    Column('due_date', DateTime),
    Column('is_done', Boolean),
    Column('body', String(length=500)),
    Column('user_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].drop()
    post_meta.tables['contact'].create()
    post_meta.tables['conversation'].create()
    post_meta.tables['task'].create()
    pre_meta.tables['user'].columns['nickname'].drop()
    post_meta.tables['user'].columns['first_name'].create()
    post_meta.tables['user'].columns['last_name'].create()
    post_meta.tables['user'].columns['password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].create()
    post_meta.tables['contact'].drop()
    post_meta.tables['conversation'].drop()
    post_meta.tables['task'].drop()
    pre_meta.tables['user'].columns['nickname'].create()
    post_meta.tables['user'].columns['first_name'].drop()
    post_meta.tables['user'].columns['last_name'].drop()
    post_meta.tables['user'].columns['password'].drop()
