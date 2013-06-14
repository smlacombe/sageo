from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, \
    Required

class LoginForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me', default=False)
