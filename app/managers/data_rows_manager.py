from app.db_model.view import View
from app.db_model.base import db_session
from app.db_model.viewColumn import ViewColumn
from app.lib import livestatus_query
from app.lib.datasources import multisite_datasources as datasources
from app.lib.multi_keys_sorting import compose, multikeysort
from app.managers.filters_manager import FiltersManager
from app.managers.view_manager import ViewManager
from app.model.columns.builtin import painters
import copy
from operator import itemgetter, methodcaller

class DataRowsManager():
    """ A sort of proxy that facilitate gathering data from LiveStatus without knowing implementation details. """
    def __init__(self):
        self.__view_manager = None
        self.__filters_manager = None
    '''
    Set the view with the link_name. If a view is found, return true, else return false.
    '''
    def set_view(self, link_name):
        self.__view_manager = ViewManager()
        if self.__view_manager.set_view(link_name):
            self.__filters_manager = FiltersManager()
            self.update_filters()
            return True
        else:
            return False

    def update_filters(self):
        self.__filters_manager.set_filters(self.__view_manager.get_filters())

    def get_rows(self):
        """ get rows corresponding to the query builded with the view and its options """
        # prepare basic parameter datasource and columns_name
        datasource = datasources[self.__view_manager.get_view().datasource]        
        columns_name = self.get_asked_columns_name()
        filters_string = self.__filters_manager.get_filter_query() 
        print '\nfilters: ' + filters_string
        rows = self.__readable_rows(livestatus_query.get_rows(datasource, columns_name, filters_string))         
        sorters = self.__view_manager.get_sorters()
        if sorters:
            arguments = []
            callers = {}
            for sorter in sorters:
                prefix = ''
                if sorter.sorter_option == '1':
                    prefix = '-'
                arguments.append(prefix + sorter.column)
                get_lower = compose(itemgetter(sorter.column), methodcaller('lower')) 
                callers[sorter.column] = get_lower
            sortedRows = multikeysort(rows, arguments, callers)
            return sortedRows
        return rows

    def __readable_rows(self, rows):
        rows_readable = rows 
        for row in rows_readable:
            for name, value in row.items():
                if name in painters.keys():
                    row[name] = painters[name].get_readable(row)
        return rows_readable
                

    def get_asked_columns_name(self):
        columns_names = []
        for column in self.__view_manager.get_columns(): columns_names.append(column.column)
        return columns_names

    def get_asked_columns_title(self):
        columns_names = []
        for column in self.__view_manager.get_columns(): columns_names.append(painters[column.column].title)
        return columns_names
    
    def set_extra_filters(self, filters):
        self.__view_manager.set_filters(filters)
        self.update_filters()

    def get_filters_name(self):
        return self.__filters_manager.get_filters_name()
    
    def get_view(self):
        return self.__view_manager.get_view()
