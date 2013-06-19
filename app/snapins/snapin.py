import abc

class SnapinBase(object):
    __metaclass__ = abc.ABCMeta
    __title = "snapin title"
    __description = "snapin description" 
    __version = "0.0"
    __name = "default snapin"
    
    @abc.abstractmethod
    def context(self):
        """Return some stuff to be used in the snapin template"""
        return ""
