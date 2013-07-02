from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
_ = lazy_gettext


from flask.ext.wtf import FieldList, Form, FormField, TextField, IntegerField, SelectField, RadioField, PasswordField, BooleanField, \
    Required
from app.forms.libforms import TranslatedForm 

class LoginForm(TranslatedForm):
    username = TextField(_(u'Username:'), validators=[Required()])
    password = PasswordField(_(u'Password:'), validators=[Required()])
    remember = BooleanField(_(u'Remember me'), default=False)

