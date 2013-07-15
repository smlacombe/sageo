from .filter import Filter

STATE_CODES = { 'UP': 0 , "DOWN": 1 , "UNREACH": 2, "PENDING": 3 }

class FilterHostState(Filter):
    def __init__(self, name, title, descr):
        Filter.__init__(self, name, title, descr) 

    def filter(self, states):
        """
            Filter host states.
            states: dictionnary that contain states and is boolean value
        """
        filter = "Filter: host_has_been_checked = 1\n"  
        state_code = 0
        count = 0
        for state, value in states.items():
            if value:
                state_code = STATE_CODES[state]  
                filter = filter + "Filter: host_state = " + str(state_code) + "\n"
                count = count + 1
       
        filter = filter + "Or: " + str(count) + "\n"  
        return filter
