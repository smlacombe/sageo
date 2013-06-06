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


import os

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

from controllers.login import mod_auth
from controllers.index import mod_main
from controllers.side import mod_side
from flaskext.babel import Babel

# Configuration
os.environ['FLASKR_SETTINGS'] = 'sageo.cfg'

app = Flask(__name__, static_folder="static")
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=False)
babel = Babel(app)
#import ipdb;ipdb.set_trace()

@babel.localeselector
def get_locale():
    return 'fr'


@app.route('/images/<path:filename>')
def send_image(filename):
    return app.send_static_file("images/"+filename)

# Module
#import ipdb;ipdb.set_trace()
app.register_module(mod_auth)
app.register_module(mod_main)
app.register_module(mod_side)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
