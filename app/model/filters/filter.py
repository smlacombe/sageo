import abc

class Filter:
    """
    Base class for all filters
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, title, info, column_name):
        self.name = name
        self.info = info
        self.title = title
        self.column_name = column_name

    @abc.abstractmethod
    def filter(self, column_value)
        """ return filter string """
