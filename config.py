# -*- coding: utf-8 -*- 
import os
basedir = os.path.abspath(os.path.dirname(__file__))
# Flask
DEBUG = True
SECRET_KEY = 'development key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
CSRF_ENABLED = True

MAX_SORTING_COLUMNS = 5

LANGUAGES = {
    'en': u'English',
    'fr': u'Français'
}

SITES = {
  "Mac mini": {
     "alias":          "Shinken mac mini",
     "socket":         "tcp:192.168.50.137:50000",
     "url_prefix":     "http://192.168.50.137",
   },
  "Production": {
     "alias":          "Shinken prod",
     "socket":         "tcp:192.168.52.44:50000",
     "url_prefix":     "http://192.168.52.44",
   },

}

