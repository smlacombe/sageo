from flask.ext.wtf import FieldList, Form, FormField, TextField, IntegerField, SelectField, RadioField, PasswordField, BooleanField, \
    Required
from app.forms.libforms import TranslatedForm
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
_ = lazy_gettext
from app import babel, app

class ProfileForm(TranslatedForm):
    #language = SelectField(_(u'Language'), choices=[("fr","Francais"), ("en","English")])
    language = SelectField(_(u'Language'), choices=[(lang_code, lang_name) for lang_code, lang_name in app.config['LANGUAGES'].iteritems()])
