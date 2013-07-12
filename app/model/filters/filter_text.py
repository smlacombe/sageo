from .filter import Filter

class FilterText(Filter):
    def __init__(self, name, title, info, descr, column_name, operation):
        Filter.__init__(self, name, title, info, descr)
        self.operation = operation
        self.column_name = column_name

    def filter(self, column_value):
        if column_value:
             return "Filter: %s %s %s\n" % (self.column_name, self.operation, column_value)
        else:
            return ""
