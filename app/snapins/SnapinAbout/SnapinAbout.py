from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Module, current_app 
from flask.ext.babelex import Domain, gettext, ngettext 

import abc
from ..snapin import SnapinBase
from app import babel, app
import os

class SnapinAbout(SnapinBase):
    def __init__(self):
        self.mydomain = Domain(os.path.abspath('app/snapins/SnapinAbout/translations'))
        _ = self.mydomain.lazy_gettext
        self.title = _(u'About Sageo')
        self.description = "Version information and Links to Documentation, Homepage and Download of Check_MK"
        self.version = "0.1"
        self.name = "about"
 
    def context(self):
        return self.description
