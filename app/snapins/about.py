from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Module, current_app 
from flaskext.babel import gettext, ngettext 

snapin_properties = {}
snapin_properties['title'] = "About Check_MK"
snapin_properties['description'] = "Version information and Links to Documentation, Homepage and Download of Check_MK"
snapin_properties['version'] = "0.1"
snapin_properties['name'] = "about"

def snapin_about():
    return {} 

