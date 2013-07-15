from app.db_model.view import View
from app.db_model.base import db_session
from app.db_model.viewColumn import ViewColumn
from app.lib import livestatus_query
from app.lib.datasources import multisite_datasources as datasources
from app.managers.filters_manager import FiltersManager


class DataRowsManager():
    """ A sort of proxy that facilitate gathering data from LiveStatus without knowing implementation details. """
    def __init__(self):
        self.__view = None
        self.__columns = None 
        self.__rows = None
        self.__filters_manager = None
    '''
    Set the view with the link_name. If a view is found, return true, else return false.
    '''
    def set_view(self, link_name):
        self.__view = View.query.filter_by(link_name=link_name).first()
        if self.__view:
            self.__columns = ViewColumn.query.filter_by(parent_id=self.__view.id).all()
            self.__filters_manager = FiltersManager()
            self.__filters_manager.set_filters(self.__view.get_filters())
            return True
        else:
            return False

    def get_rows(self):
        """ get rows corresponding to the query builded with the view and its options """
        # prepare basic parameter datasource and columns_name
        datasource = datasources[self.__view.datasource]        
        columns_name = self.get_asked_columns_names()
        filters_string = self.__filters_manager.get_filter_query() 
        print '\nfilters: ' + filters_string
        return livestatus_query.get_rows(datasource, columns_name, filters_string)         

    def get_asked_columns_names(self):
        columns_names = []
        for column in self.__columns: columns_names.append(column.column)
        return columns_names

    def get_columns(self):
        return self.__columns
    
    def get_view(self):
        return self.__view
