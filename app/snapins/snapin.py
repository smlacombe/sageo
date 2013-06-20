import abc

class SnapinBase(object):
    __metaclass__ = abc.ABCMeta
    title = "snapin title"
    description = "snapin description" 
    version = "0.0"
    name = "default snapin"
    
    @abc.abstractmethod
    def context(self):
        """Return some stuff to be used in the snapin template"""
        return ""
