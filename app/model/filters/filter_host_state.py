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


from .filter import Filter
from builtin import FILTER_HOST_STATE 
from sqlalchemy import *
from sqlalchemy.orm import *

STATE_CODES = { FILTER_HOST_STATE + '_up': 0 , FILTER_HOST_STATE + '_down': 1 , FILTER_HOST_STATE + '_unreach': 2, FILTER_HOST_STATE + '_pending': 3 } 

class FilterHostState(Filter): 
    def __init__(self, name, title, descr): 
        Filter.__init__(self, name, title, descr) 
        self.column_names = ['host_has_been_checked', 'host_state']
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

    def get_col_def(self):
        return [
                    Column(FILTER_HOST_STATE + '_up', Boolean, default=True, info={'label': 'UP'}),
                    Column(FILTER_HOST_STATE + '_down', Boolean, default=True, info={'label': 'DOWN'}),
                    Column(FILTER_HOST_STATE + '_unreach', Boolean, default=True, info={'label': 'UNREACHABLE'}),
                    Column(FILTER_HOST_STATE + '_pending', Boolean, default=True, info={'label': 'PENDING'})
                ]

