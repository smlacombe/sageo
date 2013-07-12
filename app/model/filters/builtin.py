from flask.ext.babelex import gettext, ngettext
from app import app
from app.model.filters.filter import Filter
from app.model.filters.filter_text import FilterText
from app.model.filters.filter_host_state import FilterHostState

OP_EQUAL = '='
OP_TILDE = '~~'

FILTER_HOSTREGEX = 'hostregex'
FILTER_EXACT_MATCH = 'host'
FILTER_HOSTSTATE = 'hoststate'

filters = {}

# Text filters

filters[FILTER_HOSTREGEX] = FilterText(FILTER_HOSTREGEX,    _("Hostname"),        "host",   _("Search field allowing regular expressions and partial matches"), "host_name", OP_TILDE) 
filters[FILTER_EXACT_MATCH] = FilterText(FILTER_EXACT_MATCH, _("Hostname (exact match)"), "host", _("Exact match, used for linking"), "host_name", OP_EQUAL)
filters[FILTER_HOSTATE] = FilterHostState.__init__(self, "hoststate", _("Host states"), "host") 
