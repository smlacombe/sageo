from flask.ext.babelex import gettext, ngettext
from app import app
from .column_painter_last_event import ColumnPainterLastEvent
from .column_painter_state import ColumnPainterState
from .column_painter_raw import ColumnPainterRaw

COL_HOST_NAME = 'host_name'
COL_HOST_STATE = 'host_state'
COL_SERVICE_STATE = 'service_state'
COL_LAST_CHECK = 'last_check'
COL_CHECK_COMMAND = 'check_command'
COL_SITE = 'site'
COL_SERVICE_DESCRIPTION = 'service_description'
COL_SERVICE_PLUGIN_OUTPUT = 'service_plugin_output'
COL_STATE_TYPE = 'state_type'

_ = gettext
painters = {}

painters[COL_HOST_NAME] = ColumnPainterRaw(COL_HOST_NAME, _(u'Host name'), _(u'Host name'), ['hosts', 'services']) 

nagios_host_states = {0 : 'UP', 1: 'DOWN', 2: 'UNREACHABLE'}
painters[COL_HOST_STATE] = ColumnPainterState(COL_HOST_STATE, _(u'Host state'), _(u'Host state'), ['hosts', 'services'], nagios_host_states)

nagios_service_states = {0 : 'OK', 1: 'WARNING', 2: 'CRITICAL', 3: 'UNKNOWN'}
painters[COL_SERVICE_STATE] = ColumnPainterState(COL_SERVICE_STATE, _(u'Service state'), _(u'Service state'), ['services'], nagios_service_states)

nagios_state_type = {0: 'SOFT', 1: 'HARD'}
painters[COL_STATE_TYPE] = ColumnPainterState(COL_STATE_TYPE, _(u'State type'), _(u'State type'), ['services', 'hostsbygroup', 'servicesbygroup','servicesbyhostgroup', 'log', 'hosts'], nagios_state_type)


painters[COL_LAST_CHECK] = ColumnPainterLastEvent(COL_LAST_CHECK, _(u'Last check'), _(u'Last check'), ['hosts', 'services'])
painters[COL_CHECK_COMMAND] = ColumnPainterRaw(COL_CHECK_COMMAND, _(u'Check command'), _(u'Check command'), ['hosts', 'services'])
painters[COL_SITE] = ColumnPainterRaw(COL_SITE, _(u'Site'), _(u'Site'), ['hosts', 'services'])
painters[COL_SERVICE_DESCRIPTION] = ColumnPainterRaw(COL_SERVICE_DESCRIPTION, _(u'Service'), _(u'Service'), ['services'])
painters[COL_SERVICE_PLUGIN_OUTPUT] = ColumnPainterRaw(COL_SERVICE_PLUGIN_OUTPUT, _(u'Service output'), _(u'Service output'), ['services'])

def get_columns_pairs(datasources=None):
    column_pairs = []
    for name, col in painters.iteritems():
        if not datasources or datasources in col.datasources:
            column_pairs.append((name, col.title))
    column_pairs.append(('',''))
    return sorted(column_pairs)

def get_columns_name(datasources=None):
    column_names = []
    for name, col in painters.iteritems():
        if not datasources or datasources in col.datasources:
            column_names.append(col.name)
    column_names.append('')
    return sorted(column_names)

def get_datasources_available():
    lst_datasources = []
    for name, col in painters.iteritems():
        lst_datasources += col.datasources
    return list(set(lst_datasources))

