import abc

class ColumnPainter:
    """
    Base class for all column painters.
    A column painter provide informations on a specific column to be
    human readable.
    """
    __metaclass = abc.ABCMeta
    def __init__(self, name, title, short_title, datasources):
        self.name = name
        self.title = title
        self.short_title = short_title
        self.datasources = datasources
    
    @abc.abstractmethod
    def get_readable(self, row):
        """ return real col value """
