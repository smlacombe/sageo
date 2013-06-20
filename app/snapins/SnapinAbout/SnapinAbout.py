from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Module, current_app 
from flaskext.babel import gettext, ngettext 

import abc
from ..snapin import SnapinBase

class SnapinAbout(SnapinBase):
    title = ""
    def __init__(self):
        self.title = "About Sageo"
        self.description = "Version information and Links to Documentation, Homepage and Download of Check_MK"
        self.version = "0.1"
        self.name = "about"
 
    def context(self):
        return self.description
