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

class ViewFiltersForm(ModelForm, TranslatedFormNoCsrf):
    class Meta:
        model = ViewFilters
    
    def get_filters(self):
        filters = ViewFilters()
        for col, value in self.data.iteritems():
            setattr(filters, col, value)
        return filters

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
        return self.filters.get_filters()  
