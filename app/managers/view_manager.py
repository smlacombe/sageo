from app.db_model.view import View
from app.db_model.base import db_session
from app.db_model.viewColumn import ViewColumn
from app.lib import livestatus_query
from app.lib.datasources import multisite_datasources as datasources
from app.managers.filters_manager import FiltersManager
from app.model.columns.builtin import painters
import copy

class ViewManager():
    """ A sort of proxy that facilitate views modification and views queries. """
    def __init__(self):
        self.__view = None
        self.__columns = None 
        self.__filters = None
        self.__filters_manager = None
    '''
    Set the view with the link_name. If a view is found, return true, else return false.
    '''
    def set_view(self, link_name):
        self.__view = View.query.filter_by(link_name=link_name).first()
        if self.__view:
            self.__columns = ViewColumn.query.filter_by(parent_id=self.__view.id).order_by(ViewColumn.id).all()
            self.__filters = ViewFilters.query.filter_by(parent_id=self.__view.id).first()
            self.__filters_manager = FiltersManager()
            self.update_filters()
            return self.__view 
        else:
            return None

    def add_columns(self, columns, delete_before = False):
        if delete_before:
            for column in __columns:
                    db_session.delete(column)

        for column in columns:
            db_session.add(column)
        
        db_session.commit()

    def add_view(self, view):
        db_session.add(view)
        db_session.commit()

    def update_filters(self):
        self.__filters_manager.set_filters(self.__view.get_filters())

    def get_filters(self):
        return self.__filters

    def get_columns(self):
        return self.__columns
    
    def get_view(self):
        return self.__view
