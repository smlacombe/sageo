from flask.ext.wtf import Form
import wtforms.ext.i18n.form

class TranslatedForm(wtforms.ext.i18n.form.Form, Form):
    pass
