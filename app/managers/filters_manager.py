from app.model.filter.filter import Filter
from app.model.filter.filter_text import FilterText

class FiltersManager():
    """ A sort of proxy that facilitates filters usage. There is one FiltersManager per view display.
    """   
    def __init__(self):
        self.__filters
