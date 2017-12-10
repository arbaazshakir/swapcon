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
    Column('goal_target', Integer),
    Column('current_count', Integer),
    Column('next_period_start', DateTime),
    Column('is_active', Boolean),
    Column('order', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['goals'].columns['goal_target'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['goals'].columns['goal_target'].drop()
