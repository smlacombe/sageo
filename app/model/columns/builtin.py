from flask.ext.babelex import gettext, ngettext
from app import app
from .column_painter_last_event import ColumnPainterLastEvent
from .column_painter_host_state import ColumnPainterHostState
from .column_painter_raw import ColumnPainterRaw

COL_HOST_NAME = 'host_name'
COL_HOST_STATE = 'host_state'
COL_LAST_CHECK = 'last_check'
COL_CHECK_COMMAND = 'check_command'

_ = gettext
painters = {}

painters[COL_HOST_NAME] = ColumnPainterRaw(COL_HOST_NAME, _(u'Host name'), _(u'Host name'), ['hosts', 'services']) 
painters[COL_HOST_STATE] = ColumnPainterHostState(COL_HOST_STATE, _(u'Host state'), _(u'Host state'), ['hosts', 'services'])
painters[COL_LAST_CHECK] = ColumnPainterLastEvent(COL_LAST_CHECK, _(u'Last check'), _(u'Last check'), ['hosts', 'services'])
painters[COL_CHECK_COMMAND] = ColumnPainterRaw(COL_CHECK_COMMAND, _(u'Check command'), _(u'Check command'), ['hosts', 'services'])

def get_columns_pairs(datasources=None):
    column_pairs = []
    for name, col in painters.iteritems():
        if not datasources or col.datasources in datasources:
            column_pairs.append((name, col.title))
    return column_pairs

def get_columns_name(datasources=None):
    column_names = []
    for name, col in painters.iteritems():
        if not datasources or col.datasources in datasources:
            column_names.append(col.name)
    return column_names
