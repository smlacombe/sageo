from .filter import Filter

class FilterHostState(Filter):
    def __init__(self, name, title, info, descr):
        Filter.__init__(self, name, title, info, descr) 

    def filter(self, state):
        return "Filter: host_state = " + state + "\n"
