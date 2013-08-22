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

_ = gettext
OP_EQUAL = '='
OP_TILDE = '~~'
FILTER_HOSTREGEX = 'host_regex'
FILTER_HOST_EXACT_MATCH = 'host'
FILTER_SERVICE_EXACT_MATCH = 'service'
FILTER_HOST_STATE = 'host_state'
FILTER_SERVICE_STATE = 'service_state'
FILTER_IS_SUMMARY_HOST = 'is_summary_host'
FILTER_SITE = 'site'
FILTER_IS_HOST_ACKNOWLEDGED = 'is_host_acknowledged'
FILTER_IS_SERVICE_ACKNOWLEDGED = 'is_service_acknowledged'
FILTER_IS_HOST_IN_NOTIFICATION_PERIOD = 'is_host_in_notification_period'
FILTER_IS_SERVICE_IN_NOTIFICATION_PERIOD = 'is_service_in_notification_period'
FILTER_IS_HOST_SCHEDULED_DOWNTIME_DEPTH = 'is_host_scheduled_downtime_depth'
FILTER_IS_SERVICE_SCHEDULED_DOWNTIME_DEPTH = 'is_service_scheduled_downtime_depth'

from app.model.filters.filter import Filter
from app.model.filters.filter_text import FilterText
from app.model.filters.filter_host_state import FilterHostState
from app.model.filters.filter_service_state import FilterServiceState
from app.model.filters.filter_nagios_expr import FilterNagiosExpr
from app.model.filters.filter_nagios_flag import FilterNagiosFlag
from app.model.filters.filter_site import FilterSite



filters = {}

# Text filters

filters[FILTER_HOST_EXACT_MATCH] = FilterText(FILTER_HOST_EXACT_MATCH, _("Hostname (exact match)"), _("Exact match, used for linking"), ["host_name"], OP_EQUAL)
filters[FILTER_SERVICE_EXACT_MATCH] = FilterText(FILTER_SERVICE_EXACT_MATCH, _("Service description (exact match)"), _("Exact match, used for linking"), ["service_description"], OP_EQUAL)

filters[FILTER_HOSTREGEX] = FilterText(FILTER_HOSTREGEX, _("Hostname"), _("Search field allowing regular expressions and partial matches"), ["host_name"], OP_TILDE) 
filters[FILTER_SITE] = FilterSite(FILTER_SITE, _("Site"), _("Site (exact match)")) 


# State filters
filters[FILTER_HOST_STATE] = FilterHostState(FILTER_HOST_STATE, _("Host states"), _("Filter host state")) 
filters[FILTER_SERVICE_STATE] = FilterServiceState(FILTER_SERVICE_STATE, _("Service states"), _("Filter service state"))

# Nagios expression filters
filters[FILTER_IS_SUMMARY_HOST] = FilterNagiosExpr(FILTER_IS_SUMMARY_HOST, _("Is summary host"), '', '0', ['host_custom_variable_names'], "Filter: host_custom_variable_names >= _REALNAME\n", "Filter: host_custom_variable_names < _REALNAME\n") 


#Nagios flag filters

filters[FILTER_IS_HOST_ACKNOWLEDGED] = FilterNagiosFlag(FILTER_IS_HOST_ACKNOWLEDGED,  _("Host problem has been acknowledged"), '', default='-1', column=['host_acknowledged'])
filters[FILTER_IS_SERVICE_ACKNOWLEDGED] = FilterNagiosFlag(FILTER_IS_SERVICE_ACKNOWLEDGED,  _("Service problem has been acknowledged"), '', default='-1', column=['service_acknowledged'])
filters[FILTER_IS_HOST_IN_NOTIFICATION_PERIOD] = FilterNagiosFlag(FILTER_IS_HOST_IN_NOTIFICATION_PERIOD,  _("Host in notif. period"), '', default='-1', column=['host_in_notification_period']) 
filters[FILTER_IS_SERVICE_IN_NOTIFICATION_PERIOD] = FilterNagiosFlag(FILTER_IS_SERVICE_IN_NOTIFICATION_PERIOD,  _("Service in notif. period"), '', default='-1', column=['service_in_notification_period']) 
filters[FILTER_IS_HOST_SCHEDULED_DOWNTIME_DEPTH] = FilterNagiosFlag(FILTER_IS_HOST_SCHEDULED_DOWNTIME_DEPTH,  _("Host in downtime"), '', default='-1', column=['host_scheduled_downtime_depth']) 
filters[FILTER_IS_SERVICE_SCHEDULED_DOWNTIME_DEPTH] = FilterNagiosFlag(FILTER_IS_SERVICE_SCHEDULED_DOWNTIME_DEPTH,  _("Service in downtime"), '', default='-1', column=['service_scheduled_downtime_depth']) 
