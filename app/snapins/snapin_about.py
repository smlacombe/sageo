from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Module, current_app 
from flaskext.babel import gettext, ngettext 

import abc
from snapin import SnapinBase

class SnapinAbout(object):
    __title = "About Check_MK"
    __description = "Version information and Links to Documentation, Homepage and Download of Check_MK"
    __version = "0.1"
    __name = "about"
     
    def context(self):
        return ""
