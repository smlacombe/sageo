import os

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
app = Flask(__name__)

from controllers.login import *

# Configuration
os.environ['FLASKR_SETTINGS'] = 'sageo.cfg'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=False)
print app.config['USERNAME']

#if __name__ == "__main__":
#    app.run()
