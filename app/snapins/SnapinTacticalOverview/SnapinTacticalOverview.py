#   
#   Copyright (C) 2013
#     Mathias Kettner, mk@mathias-kettner.de
#     Savoir-Faire Linux Inc.
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


from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Module, current_app
from flask.ext.babelex import Domain, gettext, ngettext
import abc
from ..snapin import SnapinBase
from app.lib.livestatusconnection import live
from os import path

class SnapinTacticalOverview(SnapinBase):
    def __init__(self):
        self.translations_path = path.join(path.dirname(__file__), 'translations') 
        self.mydomain = Domain(self.translations_path)
        _ = self.mydomain.lazy_gettext
        self.title = _(u'Tactical overview')
        self.description = _(u'The total number of hosts and service with and without problems')
        self.version = "0.1"
        self.name = "tactical_overview"
    
    def context(self): 
        context = {}
        host_query = \
            "GET hosts\n" \
            "Stats: state >= 0\n" \
            "Stats: state > 0\n" \
            "Stats: scheduled_downtime_depth = 0\n" \
            "StatsAnd: 2\n" \
            "Stats: state > 0\n" \
            "Stats: scheduled_downtime_depth = 0\n" \
            "Stats: acknowledged = 0\n" \
            "StatsAnd: 3\n" \
            "Filter: custom_variable_names < _REALNAME\n"

        service_query = \
            "GET services\n" \
            "Stats: state >= 0\n" \
            "Stats: state > 0\n" \
            "Stats: scheduled_downtime_depth = 0\n" \
            "Stats: host_scheduled_downtime_depth = 0\n" \
            "Stats: host_state = 0\n" \
            "StatsAnd: 4\n" \
            "Stats: state > 0\n" \
            "Stats: scheduled_downtime_depth = 0\n" \
            "Stats: host_scheduled_downtime_depth = 0\n" \
            "Stats: acknowledged = 0\n" \
            "Stats: host_state = 0\n" \
            "StatsAnd: 5\n" \
            "Filter: host_custom_variable_names < _REALNAME\n"
        context['toggle_url'] = "sidebar_openclose.py?name=%s&state=" % 'tactical_overview' 

        context['hstdata'] = live.query_summed_stats(host_query)
        context['svcdata'] = live.query_summed_stats(service_query)

        return context
