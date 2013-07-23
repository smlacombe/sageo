from flask.ext.babelex import gettext, ngettext
from app import app

_ = gettext
OP_EQUAL = '='
OP_TILDE = '~~'
FILTER_HOSTREGEX = 'host_regex'
FILTER_EXACT_MATCH = 'host'
FILTER_HOST_STATE = 'host_state'
FILTER_IS_SUMMARY_HOST = 'is_summary_host'

from app.model.filters.filter import Filter
from app.model.filters.filter_text import FilterText
from app.model.filters.filter_host_state import FilterHostState
from app.model.filters.filter_nagios_expr import FilterNagiosExpr


filters = {}

# Text filters

filters[FILTER_HOSTREGEX] = FilterText(FILTER_HOSTREGEX,    _("Hostname"), _("Search field allowing regular expressions and partial matches"), "host_name", OP_TILDE) 
filters[FILTER_EXACT_MATCH] = FilterText(FILTER_EXACT_MATCH, _("Hostname (exact match)"), _("Exact match, used for linking"), "host_name", OP_EQUAL)

# State filters
filters[FILTER_HOST_STATE] = FilterHostState(FILTER_HOST_STATE, _("Host states"), _("Filter host state")) 

# Nagios expression filters
filters[FILTER_IS_SUMMARY_HOST] = FilterNagiosExpr(FILTER_IS_SUMMARY_HOST, _("Is summary host"), '', "Filter: host_custom_variable_names >= _REALNAME\n", "Filter: host_custom_variable_names < _REALNAME\n") 


