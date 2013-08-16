from .filter import Filter
from builtin import FILTER_SERVICE_STATE
from sqlalchemy import *
from sqlalchemy.orm import *

STATE_CODES = { FILTER_SERVICE_STATE + '_ok': 0 , FILTER_SERVICE_STATE + '_warning': 1 , FILTER_SERVICE_STATE + '_critical': 2, FILTER_SERVICE_STATE + '_unknown': 3 }

class FilterServiceState(Filter):
    def __init__(self, name, title, descr):
        Filter.__init__(self, name, title, descr)
        self.column_names = ['service_has_been_checked', 'service_state']
    def filter(self, states):
        """
            Filter service states.
            states: dictionnary that contain states and is boolean value
        """
        filter = "Filter: service_has_been_checked = 1\n"
        state_code = 0
        count = 0
        for state, value in states.items():
            if value:
                state_code = STATE_CODES[state]
                filter = filter + "Filter: service_state = " + str(state_code) + "\n"
                count = count + 1

        filter = filter + "Or: " + str(count) + "\n"
        return filter

    def get_col_def(self):
        return [
                    Column(FILTER_SERVICE_STATE + '_ok', Boolean, default=True, info={'label': 'OK'}),
                    Column(FILTER_SERVICE_STATE + '_warning', Boolean, default=True, info={'label': 'WARNIN'}),
                    Column(FILTER_SERVICE_STATE + '_critical', Boolean, default=True, info={'label': 'CRITICAL'}),
                    Column(FILTER_SERVICE_STATE + '_unknown', Boolean, default=True, info={'label': 'UNKNOWN'})
                ]
