from sqlalchemy import *
from sqlalchemy.orm import *
from app.db_model.base import Base
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
from app.db_model.view import View
_ = lazy_gettext

column_choices = [('host_name',_(u'Hostname')),('host_state',_(u"Host state")), ('last_check',_(u"Last check"))]

class ViewColumn(Base):
    __tablename__ = 'view_column'
    id = Column(Integer, primary_key=True)
    column = Column(Enum('host_name', 'host_state', 'last_check'), info={'choices':column_choices} )
    parent_id = Column(Integer, ForeignKey(View.id), nullable=False)
    view = relationship(
        View,
        backref = 'view_column'
    )
