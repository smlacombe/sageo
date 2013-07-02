from flask.ext.wtf import FieldList, Form, FormField, TextField, IntegerField, SelectField, RadioField, PasswordField, BooleanField, \
    Required
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
_ = lazy_gettext
from app.forms.libforms import TranslatedForm
from wtforms_alchemy import ModelForm, ModelFieldList
from app.models import View, ViewColumn


filter_choices = [('off',_(u'Don''t use')),('hard',_(u"Hardcode")),('show',_(u"Show to user")), ('hide',_(u"Use for linking"))]
datasource_choices = [('allhost',_(u'All hosts')),('allservices',_(u"All services"))]
column_choices = [('hostname',_(u'Hostname')),('hoststate',_(u"Host state")), ('lastcheck',_(u"Last check"))]

class ViewColumnForm(ModelForm, TranslatedForm):
    class Meta:
        model = ViewColumn

class ViewForm(ModelForm, TranslatedForm):
    class Meta:
        model = View

    columns = ModelFieldList(FormField(ViewColumnForm))
    summary = RadioField('Summary', choices=[('yes',_(u'Yes')),('no',_(u'No')),('ignore',_(u'Ignore'))], default='no')

################# BasicSettingsForm ###################### 
class BasicSettingsForm(TranslatedForm):
    title = TextField(_(u'Title'), validators=[Required()])
    link_name = TextField(_(u'Link Name'), validators=[Required()])
    datasource = SelectField(_(u'Datasource'), choices=datasource_choices)
    buttontext = TextField(_(u'Buttontext'))
    reload_intervall = IntegerField(_(u'Browser reload intervall'), default=30)

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

'''
class ViewForm(TranslatedForm):
    basic_settings = FormField(BasicSettingsForm)
    filters = FormField(FiltersForm)
    layout = FormField(LayoutForm)
    columns = FieldList(FormField(Column))
'''
