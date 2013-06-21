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

        try:
            context['hstdata'] = live.query_summed_stats(host_query)
            context['svcdata'] = live.query_summed_stats(service_query)
        except livestatus.MKLivestatusNotFoundError:
            return "<center>No data from any site</center>"

        return context
