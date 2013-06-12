#   
#   Copyright (C) 2013 Savoir-Faire Linux Inc.
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Module, current_app
import lib.auth
import snapins

mod_side = Module(__name__)
sageo = current_app

def side():
    snapin_context = {}
    snapins_contexts = {} 
    for snapin in snapins.__all__: 
        __import__('snapins.' + snapin)
        snapin_context['properties'] = getattr(getattr(snapins, snapin), 'snapin_properties')
        snapin_context['context']    = getattr(getattr(snapins, snapin), 'snapin_' + snapin)() 
        snapins_contexts[snapin] = snapin_context 
        
    return snapins_contexts 

