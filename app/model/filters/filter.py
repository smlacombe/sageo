import abc

class Filter:
    """
    Base class for all filters
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, title, info, descr=''):
        self.name = name
        self.info = info
        self.descr = descr
        self.title = title

    @abc.abstractmethod
    def filter(self, column_value)
        """ return filter string """
