import os

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
app = Flask(__name__)

from controllers.login import auth
from controllers.index import main

# Configuration
os.environ['FLASKR_SETTINGS'] = 'sageo.cfg'

app = Flask(__name__, static_folder="static")
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=False)

@app.route('/images/<path:filename>')
def send_image(filename):
    return app.send_static_file("images/"+filename)

# Module
#import ipdb;ipdb.set_trace()
app.register_module(auth)
app.register_module(main)
if __name__ == "__main__":
    app.run(host='0.0.0.0')
