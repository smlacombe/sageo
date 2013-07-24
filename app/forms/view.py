from flask.ext.wtf import FieldList, Form, FormField, TextField, IntegerField, SelectField, RadioField, PasswordField, BooleanField, \
    Required
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
_ = lazy_gettext
from app.forms.libforms import TranslatedForm, TranslatedFormNoCsrf
from wtforms_alchemy import ModelForm, ModelFieldList, ModelFormField
from app.db_model.base import db_session
from app.db_model.viewColumn import ViewColumn
from app.db_model.view import View
from app.db_model.viewFilters import ViewFilters
from app.model.filters.builtin import FILTER_IS_SUMMARY_HOST

filter_choices = [('off',_(u'Don''t use')),('hard',_(u"Hardcode")),('show',_(u"Show to user")), ('hide',_(u"Use for linking"))]
datasource_choices = [('allhost',_(u'All hosts')),('allservices',_(u"All services"))]
column_choices = [('hostname',_(u'Hostname')),('hoststate',_(u"Host state")), ('lastcheck',_(u"Last check"))]

class ViewColumnForm(ModelForm, TranslatedFormNoCsrf):
    class Meta:
        model = ViewColumn

class ViewFiltersForm(ModelForm, TranslatedForm):
    class Meta:
        model = ViewFilters

setattr(ViewFiltersForm, FILTER_IS_SUMMARY_HOST, RadioField('Summary', choices=[('yes',_(u'Yes')),('no',_(u'No')),('ignore',_(u'Ignore'))], default='no'))


class ViewForm(ModelForm, TranslatedForm):
    class Meta:
        model = View

    columns = ModelFieldList(FormField(ViewColumnForm))
    filters = ModelFormField(ViewFiltersForm)    

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

    def get_filters(self):
        return filters.fdsfsd  


