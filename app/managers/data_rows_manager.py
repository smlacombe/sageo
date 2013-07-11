from app.db_model.view import View
from app.db_model.base import db_session
from app.db_model.viewColumn import ViewColumn
from app.lib import livestatus_query
from app.lib.datasources import multisite_datasources as datasources


class DataRowsManager():
    """ A sort of proxy that facilitate getting data from LiveStatus without knowing implementation details. """
    def __init__(self):
        self.__view = None
        self.__columns = None 
        self.__rows = None
        self.__filters_manager = None
    '''
    Set the view with the link_name. If a view is found, return true, else return false.
    '''
    def set_view(link_name):
        __view = View.query.filter_by(link_name=view_name).first()
        if __view:
            __columns = ViewColumn.query.filter_by(parent_id=__view.id).all()
            return true
        else
            return false

    def get_rows():
        """ get rows corresponding to the query builded with the view and its options """
        # prepare basic parameter datasource and columns_name
        datasource = datasources[__view.datasource]        
        columns_name = get_asked_columns_names() 
        

    def get_asked_columns_names():
        for column in __columns: columns_names.append(column.column)
        return columns_names

    def get_columns()
        return __columns
    
    def get_view():
        return __view
