from flask.ext.wtf import FieldList, Form, FormField, TextField, IntegerField, SelectField, RadioField, PasswordField, BooleanField, \
    Required
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
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

filter_choices = [('off',_(u'Don''t use')),('hard',_(u"Hardcode")),('show',_(u"Show to user")), ('hide',_(u"Use for linking"))]
datasource_choices = [('allhost',_(u'All hosts')),('allservices',_(u"All services"))]
column_choices = [('hostname',_(u'Hostname')),('hoststate',_(u"Host state")), ('lastcheck',_(u"Last check"))]


################# BasicSettingsForm ###################### 
class BasicSettingsForm(TranslatedForm):
    title = TextField(_(u'Title'), validators=[Required()])
    link_name = TextField(_(u'Link Name'), validators=[Required()])
    datasource = SelectField(_(u'Datasource'), choices=datasource_choices)
    buttontext = TextField(_(u'Buttontext'))
    reload_intervall = IntegerField(_(u'Browser reload intervall'), default=30)
    #topic = TextField(_(u'Topic'))
#   description = TextAreaField(_(u'Description'), [validators.optional(), validators.length(max=300)])
  # visibility_all_users = BooleanField(_(u'make this view available for all users'), default=False)
  # visibility_data_on_search = BooleanField(_(u'show data only on search'), default=False)
  # visibility_not_show_context_button = BooleanField(_(u'do not show a context button to this view'), default=False)

########## Filter Form ###################
class HostStatesFilterForm(TranslatedForm):
    options = SelectField(_(u'Host states'), choices=filter_choices)
    up = BooleanField(_(u'UP'), default=True) 
    down = BooleanField(_(u'DOWN'), default=True)
    unreach = BooleanField(_(u'UNREACH'), default=True)
    pending = BooleanField(_(u'PENDING'), default=True)

class HostnameFilterForm(TranslatedForm):
    options = SelectField(_(u'Hostname options'), choices=filter_choices)
    exact_match = BooleanField(_(u'Exact match'), default=False) 
    hostname = TextField(_(u'Hostname'))

class SummaryHostForm(TranslatedForm):
    options = SelectField(_(u'Is summary host'), choices=filter_choices)
    summary = RadioField('Summary', choices=[('yes',_(u'Yes')),('no',_(u'No')),('ignore',_(u'Ignore'))], default='no')

class FiltersForm(TranslatedForm):
    hostname = FormField(HostnameFilterForm)
    hoststates = FormField(HostStatesFilterForm)
    summaryhost = FormField(SummaryHostForm)
##################### Layout form ###############################
class LayoutForm(TranslatedForm):
    number_columns = IntegerField(_(u'Number of Columns'), default=3)

class Column(TranslatedForm):
    column = SelectField(_(u'Column'), choices=column_choices)

class ViewForm(TranslatedForm):
    basic_settings = FormField(BasicSettingsForm)
    filters = FormField(FiltersForm)
    layout = FormField(LayoutForm)
    columns = FieldList(FormField(Column))

