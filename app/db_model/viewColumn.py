#   
#   Copyright (C) 2013 Savoir-Faire Linux Inc.
#   
#   This file is part of Sageo
#   
#   Sageo is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Sageo is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Sageo.  If not, see <http://www.gnu.org/licenses/>


from sqlalchemy import *
from sqlalchemy.orm import *
from app.db_model.base import Base
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
from app.db_model.view import View
from app.model.columns.builtin import get_columns_pairs
from app.model.columns.builtin import get_columns_name
import ast
_ = lazy_gettext

column_choices = get_columns_pairs() 
column_names = get_columns_name()
if ('','') in column_choices:
    column_choices.remove(('',''))
if '' in column_names:
    column_names.remove('')
enum_col = Enum(*column_names) 

class ViewColumn(Base):
    __tablename__ = 'view_column'
    id = Column(Integer, primary_key=True)
    column = Column(enum_col, nullable=False, info={'choices':column_choices, 'label':_(u'Column')} )
    link = Column(String(30)) 
    parent_id = Column(Integer, ForeignKey(View.id), nullable=False)
    view = relationship(
        View,
        backref = 'view_column'
    )

