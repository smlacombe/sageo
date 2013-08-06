from .column_painter import ColumnPainter
import time
from flask.ext.babelex import format_timedelta
from flask.ext.babelex import format_datetime
from flask.ext.babelex import format_time
from datetime import datetime

class ColumnPainterLastEvent(ColumnPainter):
    """
    Column painter that print age for timestamp column like last_check
    """
    def get_readable(self, row):
        age = time.time() - row[self.name]
        return format_datetime(datetime.fromtimestamp(row[self.name])) 


