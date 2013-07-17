from .column_painter import ColumnPainter

class ColumnPainterRaw(ColumnPainter):
    """
    Column painter that don't need value transformation to be human readable: Ex: host_name
    """
    def __init__(self, name, title, short_title):
        ColumnPainter.__init__(self, name, title, short_title) 
    
    def get_readable(self, row):
        return row[self.name]
