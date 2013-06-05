from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Module, current_app
from flaskext.babel import gettext, ngettext

_ = gettext
auth = Module(__name__)
sageo = current_app

@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
  #      import pdb;pdb.set_trace()
        if request.form['_username'] == '' or request.form['_password'] == '':
            error = _(u'no credentials entered')
        elif request.form['_username'] != sageo.config['USERNAME']:
            error = _(u'invalid username')
        elif request.form['_password'] != sageo.config['PASSWORD']:
            error = _(u'invalid password')
        else:
#            import ipdb;ipdb.set_trace() 
            session['username'] = request.form['_username'] 
            session['logged_in'] = True
            flash(_(u'You were logged in'))
            return redirect('/')
    return render_template('users/login.html', version='0.1',error=error)

@auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(_(u'You were logged out'))
    return redirect(url_for('show_entries'))
