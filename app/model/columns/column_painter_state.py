from .column_painter import ColumnPainter

class ColumnPainterState(ColumnPainter):
    """
    Column painter that don't need value transformation to be human readable: Ex: host_name
    """

    def __init__(self, name, title, short_title, datasources, states):
        ColumnPainter.__init__(self, name, title, short_title, datasources)
        self.states = states

    def get_readable(self, row):
        return self.states[row[self.name]]
