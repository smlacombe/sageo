from flask.ext.wtf import Form, TextField, SelectField, PasswordField, BooleanField, \
    Required
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
import ipdb;ipdb.set_trace()
from wtforms.ext.i18n.utils import DefaultTranslations 
import wtforms.ext.i18n.form
from app import babel, app
from flask import Flask
_ = lazy_gettext 

class TranslatedForm(wtforms.ext.i18n.form.Form, Form):
    pass
#    import ipdb;ipdb.set_trace()
    #LANGUAGES = ['en', 'en_GB'] 

    #def _get_translations(self):
    #        return DefaultTranslations(MyTranslations())    

class LoginForm(TranslatedForm):
        username = TextField(_(u'Username:'), validators=[Required()])
        password = PasswordField(_(u'Password:'), validators=[Required()])
        remember = BooleanField(_(u'Remember me'), default=False)

class ProfileForm(TranslatedForm):
    #language = SelectField(_(u'Language'), choices=[("fr","Francais"), ("en","English")])
    language = SelectField(_(u'Language'), choices=[(lang_code, lang_name) for lang_code, lang_name in app.config['LANGUAGES'].iteritems()])
