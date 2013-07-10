from flask.ext.wtf import FieldList, Form, FormField, TextField, IntegerField, SelectField, RadioField, PasswordField, BooleanField, \
    Required
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
_ = lazy_gettext
from app.forms.libforms import TranslatedForm, TranslatedFormNoCsrf
from wtforms_alchemy import ModelForm, ModelFieldList
from app.db_model.base import db_session
from app.db_model.viewColumn import ViewColumn
from app.db_model.view import View

filter_choices = [('off',_(u'Don''t use')),('hard',_(u"Hardcode")),('show',_(u"Show to user")), ('hide',_(u"Use for linking"))]
datasource_choices = [('allhost',_(u'All hosts')),('allservices',_(u"All services"))]
column_choices = [('hostname',_(u'Hostname')),('hoststate',_(u"Host state")), ('lastcheck',_(u"Last check"))]

class ViewColumnForm(ModelForm, TranslatedFormNoCsrf):
    class Meta:
        model = ViewColumn


class ViewForm(ModelForm, TranslatedForm):
    class Meta:
        model = View

    columns = ModelFieldList(FormField(ViewColumnForm))
    summary = RadioField('Summary', choices=[('yes',_(u'Yes')),('no',_(u'No')),('ignore',_(u'Ignore'))], default='no')

    def set_view(self, view):
        self.title.data = view.title
        self.link_name.data = view.link_name
        self.datasource.data = view.datasource
        self.buttontext.data = view.buttontext
        self.reload_intervall.data = view.reload_intervall 
        self.hostname_option.data = view.hostname_option
        self.hostname_exact_match.data = view.hostname_exact_match
        self.hostname.data = view.hostname
        self.hoststate_option.data = view.hoststate_option
        self.hoststate_up.data = view.hoststate_up
        self.hoststate_down.data = view.hoststate_down
        self.hoststate_unreach.data = view.hoststate_unreach 
        self.hoststate_pending.data = view.hoststate_pending
        self.summary_option.data = view.summary_option
        self.summary.data = view.summary
        self.layout_number_columns.data = view.layout_number_columns

    def set_columns(self, columns):
        for column in columns:
            self.columns.append_entry(column) 

    def get_view(self):
        view = View()
        view.title = self.title.data
        view.link_name = self.link_name.data
        view.datasource = self.datasource.data
        view.buttontext = self.buttontext.data
        view.reload_intervall = self.reload_intervall.data
        view.hostname_option = self.hostname_option.data
        view.hostname_exact_match = self.hostname_exact_match.data
        view.hostname = self.hostname.data
        view.hoststate_option = self.hoststate_option.data
        view.hoststate_up = self.hoststate_up.data
        view.hoststate_down = self.hoststate_down.data
        view.hoststate_unreach = self.hoststate_unreach.data
        view.hoststate_pending = self.hoststate_pending.data
        view.summary_option = self.summary_option.data
        view.summary = self.summary.data
        view.layout_number_columns = self.layout_number_columns.data
        return view

    def get_columns(self, view_id):
        columns = []
        for column_form in self.columns:
            column = ViewColumn()
            column.column = column_form.column.data
            column.parent_id = view_id
            columns.append(column)
        return columns
   
 
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

##################### Layout self.###############################
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
