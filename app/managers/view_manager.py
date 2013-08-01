from app.db_model.view import View
from app.db_model.viewFilters import ViewFilters
from app.db_model.viewFilters import cache_columns
from app.db_model.base import db_session
from app.db_model.viewColumn import ViewColumn
from app.lib import livestatus_query
from app.lib.datasources import multisite_datasources as datasources
from app.managers.filters_manager import FiltersManager
from app.model.columns.builtin import painters
from app.model.filters.filter_fields_info import FilterFieldsInfo
import copy

class ViewManager():
    """ A sort of proxy that facilitate views modification and views queries. """
    def __init__(self):
        self.__view = None
        self.__columns = None 
        self.__filters = None
    '''
    Set the view with the link_name. If a view is found, return the view found 
    '''
    def set_view(self, link_name):
        self.__view = View.query.filter_by(link_name=link_name).first()
        if self.__view:
            self.__columns = ViewColumn.query.filter_by(parent_id=self.__view.id).order_by(ViewColumn.id).all()
            self.__filters = self.__view.filters 
            return self.__view 
        else:
            return None

    def add_columns(self, columns, delete_before = False):
        if delete_before:
            for column in self.__columns:
                    db_session.delete(column)

        for column in columns:
            db_session.add(column)
        
        db_session.commit()

    def add_view(self, view):
        db_session.add(view)
        db_session.commit()
        
    def add_filters(self, filters):
        self.__view.filters = filters
        db_session.commit()

    def set_filters(self, filters):
        self.__filters.set_filters(filters)

    def update_filters(self, filters):
        self.__view.filters.update(filters)
        db_session.commit()

    def get_filters(self):
        return self.__filters

    def get_columns(self):
        return self.__columns
    
    def get_filter_display(sel,form):
        lst_columns = cache_columns 
        lst_info = []
        for option, col_names in lst_columns.iteritems():
            option_field = getattr(form, option)
            fields = []
            for col in col_names: 
                fields.append(getattr(form, col))
            lst_info.append(FilterFieldsInfo(option_field, fields))
        return lst_info
    
    def get_view(self):
        return self.__view

    def update_view(self, view):
        self.__view.update_view(view)
        db_session.commit()
        
