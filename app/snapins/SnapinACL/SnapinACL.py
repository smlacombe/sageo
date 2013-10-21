#   
#   Copyright (C) 2013
#   Savoir-Faire Linux Inc.
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
from app import babel, app
from os import path

class SnapinACL(SnapinBase):
    def __init__(self):
        self.translations_path = path.join(path.dirname(__file__), 'translations')        
        self.mydomain = Domain(self.translations_path)
        _ = self.mydomain.lazy_gettext
        self.title = _(u'ACL Management')
        self.description = _(u'ACL Magement Snapin for Sageo')
        self.version = app.config["SAGEO_VERSION"]
        self.name = "acl"
 
    def context(self):
        return self.description
