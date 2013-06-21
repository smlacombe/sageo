from app.lib import livestatus
from app import app

enabled_sites = app.config['SITES'] 
live = livestatus.MultiSiteConnection(enabled_sites)
