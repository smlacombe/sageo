from .filter import Filter

class FilterNagiosExpr(Filter):
    def __init__(self, name, title, descr, pos_filter, neg_filter):
        Filter.__init__(self, name, title, descr)
        self.pos_filter = pos_filter
        self.neg_filter = neg_filter

    def filter(self, value):
        if value == 'yes':
            return self.pos_filter 
        else:
            return self.neg_filter 

