from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Module, current_app 
from flask.ext.babelex import Domain, gettext, ngettext 

import abc
from ..snapin import SnapinBase
from app import babel, app
from os import path

class SnapinAbout(SnapinBase):
    def __init__(self):
        #import ipdb;ipdb.set_trace()
        self.translations_path = path.join(path.dirname(__file__), 'translations')        
        self.mydomain = Domain(self.translations_path)
        _ = self.mydomain.lazy_gettext
        self.title = _(u'About Sageo')
        self.description = _(u'Version information and Links to Documentation, Homepage and Download of Check_MK')
        self.version = "0.1"
        self.name = "about"
 
    def context(self):
        return self.description
