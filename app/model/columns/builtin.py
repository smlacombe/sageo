from flask.ext.babelex import gettext, ngettext
from app import app
from .column_painter_age import ColumnPainterAge
from .column_painter_host_state import ColumnPainterHostState
from .column_painter_raw import ColumnPainterRaw

COL_HOST_NAME = 'host_name'
COL_HOST_STATE = 'host_state'
COL_LAST_CHECK = 'last_check'

_ = gettext
painters = {}

painters[COL_HOST_NAME] = ColumnPainterRaw(COL_HOST_NAME, _(u'Host name'), _(u'Host name')) 
painters[COL_HOST_STATE] = ColumnPainterHostState(COL_HOST_STATE, _(u'Host state'), _(u'Host state'))
painters[COL_LAST_CHECK] = ColumnPainterAge(COL_LAST_CHECK, _(u'Last check'), _(u'Last check'))
