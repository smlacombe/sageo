from flask.ext.wtf import Form, TextField, SelectField, PasswordField, BooleanField, \
    Required
from flaskext.babel import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
_ = lazy_gettext 

class LoginForm(Form):
    username = TextField(_(u'Username:'), validators=[Required()])
    password = PasswordField(_(u'Password:'), validators=[Required()])
    remember = BooleanField(_(u'Remember me'), default=False)

class ProfileForm(Form):
    #language = SelectField(_(u'Language'), choices=[("fr","Francais"), ("en","English")])
    language = SelectField(_(u'Language'), choices=[(lang_code, lang_name) for lang_code, lang_name in app.config['LANGUAGES'].iteritems()])
