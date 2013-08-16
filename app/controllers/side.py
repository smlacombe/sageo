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

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Module, current_app
import app.snapins as snapins
#from app.snapins.snapin import SnapinBase

sageo = current_app

def side():
    snapin_objects = {}
    for snapin in snapins.__all__: 
       #import ipdb;ipdb.set_trace()
       __import__('app.snapins.' + snapin + '.' + snapin)
       snapin_objects[snapin] = getattr(getattr(getattr(snapins, snapin), snapin),snapin)() 

    return snapin_objects 

