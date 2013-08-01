from .column_painter import ColumnPainter

nagios_host_states = {0 : 'UP', 1: 'DOWN', 2: 'UNREACHABLE'}

class ColumnPainterHostState(ColumnPainter):
    """
    Column painter that don't need value transformation to be human readable: Ex: host_name
    """
    def get_readable(self, row):
        return nagios_host_states[row[self.name]]
