from ..controllers import side
from flask import render_template

def render_sidebar_template(tmpl_name, **kwargs):
    snapin_objects = side.side()
    return render_template(tmpl_name, snapin_objects=snapin_objects, **kwargs)
