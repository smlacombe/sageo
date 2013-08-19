from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
view_filters = Table('view_filters', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('host_state_option', String, nullable=False),
    Column('host_state_up', Boolean),
    Column('host_state_down', Boolean),
    Column('host_state_unreach', Boolean),
    Column('host_state_pending', Boolean),
    Column('service_option', String, nullable=False),
    Column('service', String),
    Column('is_summary_host_option', String, nullable=False),
    Column('is_summary_host', String),
    Column('host_option', String, nullable=False),
    Column('host', String),
    Column('host_regex_option', String, nullable=False),
    Column('host_regex', String),
    Column('service_state_option', String, nullable=False),
    Column('service_state_ok', Boolean),
    Column('service_state_warning', Boolean),
    Column('service_state_critical', Boolean),
    Column('service_state_unknown', Boolean),
    Column('filter_site_option', String, nullable=False),
    Column('filter_site', String),
)

view_filters = Table('view_filters', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('host_state_option', Enum('off', 'hard', 'show', 'hide'), nullable=False, default=ColumnDefault('off')),
    Column('host_state_up', Boolean, default=ColumnDefault(True)),
    Column('host_state_down', Boolean, default=ColumnDefault(True)),
    Column('host_state_unreach', Boolean, default=ColumnDefault(True)),
    Column('host_state_pending', Boolean, default=ColumnDefault(True)),
    Column('service_option', Enum('off', 'hard', 'show', 'hide'), nullable=False, default=ColumnDefault('off')),
    Column('service', String(length=100)),
    Column('is_summary_host_option', Enum('off', 'hard', 'show', 'hide'), nullable=False, default=ColumnDefault('off')),
    Column('is_summary_host', Enum('yes', 'no', 'ignore'), default=ColumnDefault('no')),
    Column('host_option', Enum('off', 'hard', 'show', 'hide'), nullable=False, default=ColumnDefault('off')),
    Column('host', String(length=100)),
    Column('host_regex_option', Enum('off', 'hard', 'show', 'hide'), nullable=False, default=ColumnDefault('off')),
    Column('host_regex', String(length=100)),
    Column('service_state_option', Enum('off', 'hard', 'show', 'hide'), nullable=False, default=ColumnDefault('off')),
    Column('service_state_ok', Boolean, default=ColumnDefault(True)),
    Column('service_state_warning', Boolean, default=ColumnDefault(True)),
    Column('service_state_critical', Boolean, default=ColumnDefault(True)),
    Column('service_state_unknown', Boolean, default=ColumnDefault(True)),
    Column('filter_site_option', Enum('off', 'hard', 'show', 'hide'), nullable=False, default=ColumnDefault('off')),
    Column('site', Enum('Site 2', 'Site 1')),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['view_filters'].columns['filter_site'].drop()
    post_meta.tables['view_filters'].columns['site'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['view_filters'].columns['filter_site'].create()
    post_meta.tables['view_filters'].columns['site'].drop()
