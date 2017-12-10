from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
goals = Table('goals', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('goal_type', String(length=64)),
    Column('goal_period', String(length=64)),
    Column('current_count', Integer),
    Column('next_period_start', DateTime),
    Column('is_active', Boolean),
    Column('order', Integer),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=64)),
    Column('created', DateTime),
    Column('profile_image_url', String(length=400)),
    Column('primary_goal', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['goals'].create()
    post_meta.tables['users'].columns['primary_goal'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['goals'].drop()
    post_meta.tables['users'].columns['primary_goal'].drop()
