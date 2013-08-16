#   
#   Copyright (C) 2013 Savoir-Faire Linux Inc.
#   
#   This file is part of Sageo
#   
#   Sageo is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Sageo is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Sageo.  If not, see <http://www.gnu.org/licenses/>


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
from app.db_model.viewSorter import ViewSorter
from app.db_model.view import View
from app.db_model.viewFilters import ViewFilters
from app.db_model.viewGrouper import ViewGrouper
from app.model.filters.builtin import FILTER_IS_SUMMARY_HOST
import copy

class ViewSorterForm(ModelForm, TranslatedFormNoCsrf):
    class Meta:
        model = ViewSorter

class ViewColumnForm(ModelForm, TranslatedFormNoCsrf):
    class Meta:
        model = ViewColumn

class ViewGrouperForm(ModelForm, TranslatedFormNoCsrf):
    class Meta:
        model = ViewGrouper

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
    groupers = ModelFieldList(FormField(ViewGrouperForm))
    sorters = ModelFieldList(FormField(ViewSorterForm))
    columns_choices = None 
    filters = ModelFormField(ViewFiltersForm)    

    def set_columns(self, columns):
        for column in columns:
            self.columns.append_entry(column) 
            self.columns[-1].column.choices = copy.copy(self.columns_choices)
            if ('','') in self.columns[-1].column.choices:
                self.columns[-1].column.choices.remove(('',''))

    def set_groupers(self, groupers):
        for grouper in groupers:
            self.groupers.append_entry(grouper) 
            self.groupers[-1].column.choices = self.columns_choices

    def set_sorters(self, sorters):
        for sorter in sorters:
            self.sorters.append_entry(sorter)
            self.sorters[-1].column.choices = self.columns_choices
    
    def get_view(self):
        view = View()
        view.title = self.title.data
        view.link_name = self.link_name.data
        view.datasource = self.datasource.data
        view.buttontext = self.buttontext.data
        view.reload_intervall = self.reload_intervall.data
        view.layout_number_columns = self.layout_number_columns.data
        view.basic_layout = self.basic_layout.data
        return view
    
    def set_columns_choices(self, choices, update=False):
        self.columns_choices = choices
        if update:
            for column_form in self.columns:
                column_form.column.choices = choices 
            for sorter_form in self.sorters:
                sorter_form.column.choices = choices
            for grouper_form in self.groupers:
                grouper_form.column.choices = choices

    def get_columns(self, view_id):
        columns = []
        for column_form in self.columns:
            column = ViewColumn()
            column.column = column_form.column.data
            column.parent_id = view_id
            columns.append(column)
        return columns

    def get_groupers(self, view_id):
        groupers = []
        for grouper_form in self.groupers:
            grouper = ViewGrouper()
            grouper.column = grouper_form.column.data
            grouper.parent_id = view_id
            groupers.append(grouper)
        return groupers

    def get_sorters(self, view_id):
        sorters = []
        for sorter_form in self.sorters:
            sorter = ViewSorter()
            sorter.column = sorter_form.column.data
            sorter.sorter_option = sorter_form.sorter_option.data
            sorter.parent_id = view_id
            sorters.append(sorter)
        return sorters

    def get_filters(self):
        return self.filters.get_filters()  
