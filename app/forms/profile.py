#   
#   Copyright (C) 2013 Savoir-Faire Linux Inc.
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


from flask.ext.wtf import FieldList, Form, FormField, TextField, IntegerField, SelectField, RadioField, PasswordField, BooleanField, \
    Required
from app.forms.libforms import TranslatedForm
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
_ = lazy_gettext
from app import babel, app

class ProfileForm(TranslatedForm):
    #language = SelectField(_(u'Language'), choices=[("fr","Francais"), ("en","English")])
    language = SelectField(_(u'Language'), choices=[(lang_code, lang_name) for lang_code, lang_name in app.config['LANGUAGES'].iteritems()])
