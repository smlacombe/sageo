#   
#   Copyright (C) 2013 Savoir-Faire Linux Inc.
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Module, current_app, Blueprint
from app.lib import snapins
from flask.ext.login import LoginManager, login_user, logout_user, \
    current_user, login_required
import app.forms

index_page = Blueprint('index_page', __name__, static_folder='static', template_folder='templates')
sageo = current_app

@index_page.route('/')
@login_required
def index():
    return snapins.render_sidebar_template('main.html', current_user=current_user)
