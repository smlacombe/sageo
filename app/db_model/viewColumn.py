from sqlalchemy import *
from sqlalchemy.orm import *
from app.db_model.base import Base
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
from app.db_model.view import View
_ = lazy_gettext

filter_choices = [('off',_(u'Don''t use')),('hard',_(u"Hardcode")),('show',_(u"Show to user")), ('hide',_(u"Use for linking"))]
filter_choices_values = Enum('off','hard','show','hide')
#filter_column = Column(Enum(dict(filter_choices).keys()), info={'choices': filter_choices})
filter_column = Column(Enum('off','hard','show','hide'), info={'choices': filter_choices})
datasource_choices = [('hosts',_(u'All hosts')),('services',_(u"All services"))]
column_choices = [('host',_(u'Hostname')),('hoststate',_(u"Host state")), ('lastcheck',_(u"Last check"))]

class ViewColumn(Base):
    __tablename__ = 'view_column'
    id = Column(Integer, primary_key=True)
    column = Column(Enum('host', 'hoststate', 'lastcheck'), info={'choices':column_choices} )
    parent_id = Column(Integer, ForeignKey(View.id), nullable=False)
    view = relationship(
        View,
        backref = 'View'
    )
