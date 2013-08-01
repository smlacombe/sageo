from .column_painter import ColumnPainter

class ColumnPainterRaw(ColumnPainter):
    """
    Column painter that don't need value transformation to be human readable: Ex: host_name
    """
    def get_readable(self, row):
        return row[self.name]
