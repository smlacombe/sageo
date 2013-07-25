from .filter import Filter
from sqlalchemy import *
from sqlalchemy.orm import *

class FilterText(Filter):
    def __init__(self, name, title, descr, column_name, operation):
        Filter.__init__(self, name, title, descr)
        self.operation = operation
        self.column_name = column_name

    def filter(self, column_value):
        if column_value:
             return "Filter: %s %s %s\n" % (self.column_name, self.operation, column_value)
        else:
            return ""

    def get_col_def(self):
        return [Column(self.name, String(100), info={'label':self.title})]
