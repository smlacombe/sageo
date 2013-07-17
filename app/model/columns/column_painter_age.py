from .column_painter import ColumnPainter
import time
from flask.ext.babelex import format_timedelta


class ColumnPainterAge(ColumnPainter):
    """
    Column painter that print age for timestamp column like last_check
    """
    def __init__(self, name, title, short_title):
        ColumnPainter.__init__(self, name, title, short_title)

    def get_readable(self, row):
        age = time.time() - row[self.name]
        return time.strftime(" %H:%M:%S", time.localtime(row[self.name]))


