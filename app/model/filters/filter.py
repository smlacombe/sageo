import abc

class Filter:
    """
    Base class for all filters
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, title, descr=''):
        self.name = name
        self.descr = descr
        self.title = title

    @abc.abstractmethod
    def filter(self, value):
        """ return filter string """
