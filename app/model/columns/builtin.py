#   
#   Copyright (C) 2013 Savoir-Faire Linux Inc.
#   
#   This file is part of Sageo
#   
#   Sageo is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Sageo is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Sageo.  If not, see <http://www.gnu.org/licenses/>

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
COL_OUTPUT = 'plugin_output'
COL_NUM_SERVICES_OK = 'num_services_ok'
COL_NUM_SERVICES_WARN = 'num_services_warn'
COL_NUM_SERVICES_CRIT = 'num_services_crit'
COL_NUM_SERVICES_UNKNOWN = 'num_services_unknown'
COL_NUM_SERVICES_PENDING = 'num_services_pending'
COL_HOST_IN_NOTIFICATION_PERIOD = 'host_in_notification_period'
COL_HOST_ACKNOWLEDGED = 'host_acknowledged'
COL_HOST_SCHEDULED_DOWNTIME_DEPTH = 'host_scheduled_downtime_depth'
COL_HOST_CUSTOM_VARIABLE_NAMES = 'host_custom_variable_names'

_ = gettext
painters = {}

painters[COL_HOST_NAME] = ColumnPainterRaw(COL_HOST_NAME, _(u'Host name'), _(u'Host'), ['hosts', 'services']) 

painters[COL_OUTPUT] = ColumnPainterRaw(COL_OUTPUT, _(u'Output'), _(u'Output'), ['hosts', 'services'])


painters[COL_NUM_SERVICES_OK] = ColumnPainterRaw(COL_NUM_SERVICES_OK, _(u"Number of services in state OK"), _(u'OK'), ['hosts', 'hostgroups', 'servicegroups', 'hostsbygroup'])
painters[COL_NUM_SERVICES_WARN] = ColumnPainterRaw(COL_NUM_SERVICES_WARN, _(u"Number of services in state WARNING"), _(u'Warning'), ['hosts', 'hostgroups', 'servicegroups', 'hostsbygroup'])
painters[COL_NUM_SERVICES_CRIT] = ColumnPainterRaw(COL_NUM_SERVICES_CRIT, _(u"Number of services in state CRITICAL"), _(u'Critical'), ['hosts', 'hostgroups', 'servicegroups', 'hostsbygroup'])
painters[COL_NUM_SERVICES_UNKNOWN] = ColumnPainterRaw(COL_NUM_SERVICES_UNKNOWN, _(u"Number of services in state UNKNOWN"), _(u'UNKNOWN'), ['hosts', 'hostgroups', 'servicegroups', 'hostsbygroup'])
painters[COL_NUM_SERVICES_PENDING] = ColumnPainterRaw(COL_NUM_SERVICES_PENDING, _(u"Number of services in state PENDING"), _(u'PENDING'), ['hosts', 'hostgroups', 'servicegroups', 'hostsbygroup'])

nagios_host_states = {0 : 'UP', 1: 'DOWN', 2: 'UNREACH'}
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

yes_no_states = {0: 'no', 1: _('yes')}

painters[COL_HOST_IN_NOTIFICATION_PERIOD] = ColumnPainterState(COL_HOST_IN_NOTIFICATION_PERIOD, _(u'In notifications period'), _(u'In notif p.'), ['services', 'hostsbygroup', 'servicesbygroup','servicesbyhostgroup', 'log', 'hosts'], yes_no_states)
painters[COL_HOST_ACKNOWLEDGED] = ColumnPainterState(COL_HOST_ACKNOWLEDGED, _(u"Host problem acknowledged"), _(u'Ack'), ['services', 'hostsbygroup', 'servicesbygroup','servicesbyhostgroup', 'log', 'hosts'], yes_no_states)
painters[COL_HOST_SCHEDULED_DOWNTIME_DEPTH] = ColumnPainterRaw(COL_HOST_SCHEDULED_DOWNTIME_DEPTH, _(u'Host in dowtime'), _(u'Downtime'), ['hosts', 'services'])
painters[COL_HOST_CUSTOM_VARIABLE_NAMES] = ColumnPainterRaw(COL_HOST_CUSTOM_VARIABLE_NAMES, _(u'Custom variables names'), _(u'Custom vars'), ['hosts', 'services'])

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

