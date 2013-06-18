from flask.ext.wtf import Form, TextField, SelectField, PasswordField, BooleanField, \
    Required
from flaskext.babel import gettext, ngettext

#sageo = Flask(__name__)
_ = gettext

class LoginForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me', default=False)

class ProfileForm(Form):
#    for lang_code : language in sageo.config['LANGUAGES']:
    
    language = SelectField(_(u'Language'), choices=[("fr","Francais"), ("en","English")])
