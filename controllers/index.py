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
    abort, render_template, flash, Module, current_app
import lib.auth
import side

mod_main = Module(__name__)
sageo = current_app

@mod_main.route('/', methods=['GET'])
@lib.auth.login_required
def index():
    snapins_contexts = side.side() 
    return render_template('main.html', snapins_contexts=snapins_contexts)
