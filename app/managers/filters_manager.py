from app.model.filters.filter import Filter
from app.model.filters.filter_text import FilterText
from app.model.filters.builtin import filters 

class FiltersManager():
    """ A sort of proxy that facilitates filters usage. There is one FiltersManager per view display.
    """   
    def __init__(self):
        self.__filters = {}

    def set_filters(self, filters):
        self.__filters = filters

    def get_filter_query(self):
        filter_query = ''
        for name, filter_value in self.__filters.get_filters().iteritems():
            filter_query = filter_query + filters[name].filter(filter_value)             

        return filter_query
    
    def get_filters_name(self):
        return filters.keys()
