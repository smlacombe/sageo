from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
views = Table('views', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=30), nullable=False),
    Column('link_name', String(length=30), nullable=False),
    Column('link_title', String(length=30)),
    Column('description', Text(length=200)),
    Column('datasource', Enum('servicesbygroup', 'log', 'hosts', 'hostsbygroup', 'services', 'servicesbyhostgroup'), nullable=False),
    Column('buttontext', String(length=15)),
    Column('reload_intervall', SmallInteger, nullable=False, default=ColumnDefault(30)),
    Column('layout_number_columns', SmallInteger, nullable=False, default=ColumnDefault(3)),
    Column('basic_layout', Enum('table', 'single'), default=ColumnDefault('table')),
    Column('filters_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['views'].columns['description'].create()
    post_meta.tables['views'].columns['link_title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['views'].columns['description'].drop()
    post_meta.tables['views'].columns['link_title'].drop()
