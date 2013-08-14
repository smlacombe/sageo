from app.db_model.view import View
from app.db_model.viewFilters import ViewFilters
from app.db_model.viewSorter import ViewSorter
from app.db_model.viewGrouper import ViewGrouper
from app.db_model.viewFilters import cache_columns
from app.db_model.base import db_session
from app.db_model.viewColumn import ViewColumn
from app.lib import livestatus_query
from app.lib.datasources import multisite_datasources as datasources
from app.managers.filters_manager import FiltersManager
from app.model.columns.builtin import painters, get_columns_pairs
from app.model.filters.filter_fields_info import FilterFieldsInfo
from app.model.filters.builtin import filters
from app.model.columns.builtin import painters
import copy

class ViewManager():
    """ A sort of proxy that facilitate views modification and views queries. """
    def __init__(self):
        self.__view = None
        self.__columns = None 
        self.__groupers = None
        self.__sorters = None
        self.__filters = None
    '''
    Set the view with the link_name. If a view is found, return the view found 
    '''
    def set_view(self, link_name):
        self.__view = View.query.filter_by(link_name=link_name).first()
        if self.__view:
            self.__columns = ViewColumn.query.filter_by(parent_id=self.__view.id).order_by(ViewColumn.id).all()
            self.__groupers = ViewGrouper.query.filter_by(parent_id=self.__view.id).order_by(ViewGrouper.id).all()
            self.__sorters = ViewSorter.query.filter_by(parent_id=self.__view.id).order_by(ViewSorter.id).all()
            self.__filters = self.__view.filters 
            return self.__view 
        else:
            return None
    
    def set_view_dummy(self, datasource):
        self.__view = View()
        self.__view.datasource = datasource

    def add_columns(self, columns, delete_before = False):
        if delete_before:
            for column in self.__columns:
                    db_session.delete(column)

        for column in columns:
            db_session.add(column)
        
        db_session.commit()

    def add_groupers(self, groupers, delete_before = False):
        if delete_before:
            for grouper in self.__groupers:
                    db_session.delete(grouper)

        for grouper in groupers:
            if grouper.column:
                db_session.add(grouper)
        
        db_session.commit()

    def add_sorters(self, sorters, delete_before = False):
        if delete_before:
            for sorter in self.__sorters:
                    db_session.delete(sorter)

        for sorter in sorters:
            if sorter.column:
                db_session.add(sorter)

        db_session.commit()

    def add_view(self, view):
        db_session.add(view)
        db_session.commit()
        
    def add_filters(self, filters):
        self.__view.filters = filters
        db_session.commit()

    def set_filters(self, filters):
        self.__filters.set_filters(filters)
    
    def set_extra_sorters(self, sorters):
        for colname, order in sorters.items():
            sorter = ViewSorter()
            sorter.column = colname
            sorter.sorter_option = order
            [self.__sorters.remove(sorter_item) for sorter_item in self.__sorters if sorter_item.column == colname]
            self.__sorters.append(sorter)

    def update_filters(self, filters):
        self.__view.filters.update(filters)
        db_session.commit()

    def get_filters(self):
        return self.__filters

    def get_columns_choices(self):
        return get_columns_pairs(self.__view.datasource)

    def get_columns(self):
        return self.__columns

    def get_sorters(self):
        return self.__sorters

    def get_sorters_columns(self):
        lst_columns = []
        for sorter in self.__sorters:
            lst_columns.append(sorter.column)
        return lst_columns

    def get_groupers(self):
        return self.__groupers
    
    def get_filter_display(self, form):
        lst_columns = cache_columns 
        lst_info = []
        for option, fil_col_names in lst_columns.iteritems():
            filter_name = option.replace("_option","")
            col_names = filters[filter_name].column_names
            filter_datasources = []
            for col_name in col_names:
                if painters.has_key(col_name):
                    filter_datasources = filter_datasources + painters[col_name].datasources
                if self.__view.datasource in filter_datasources:
                    option_field = getattr(form, option)
                    fields = []
                    for col in fil_col_names: 
                        fields.append(getattr(form, col))
                    lst_info.append(FilterFieldsInfo(option_field, fields))
        return lst_info
    
    def get_view(self):
        return self.__view

    def update_view(self, view):
        self.__view.update_view(view)
        db_session.commit()
        
