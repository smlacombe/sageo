#   
#   Copyright (C) 2013
#     Mathias Kettner, mk@mathias-kettner.de
#     Savoir-Faire Linux Inc.
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


##################################################################################

from app.lib.livestatusconnection import live
from app.lib.datasources import multisite_datasources as datasources

def get_rows(datasource, columns_names, filters_string):
    # Add key columns, needed for executing commands
    columns_names += datasource["keys"]

    # Add idkey columns, needed for identifying the row
    columns_names += datasource["idkeys"] 

    # Make column list unique and remove (implicit) site column
    colset = set(columns_names)
    if "site" in colset:
        colset.remove("site")
    columns_names = list(colset)

    filters = filters_string.split("\n")
    only_sites = []
    for varFilter in filters:
        if varFilter.startswith("Sites:"):
            only_sites = varFilter.strip().split(": ")[1:]   

    rows = query_data(datasource, columns_names, '', filters_string, only_sites)
    return rows 

# Retrieve data via livestatus, convert into list of dicts,
# prepare row-function needed for painters
# datasource: the datasource key value as defined in plugins/views/datasources.py
# columns: the list of livestatus columns to query
# add_columns: list of columns the datasource is known to add itself
#  (couldn't we get rid of this parameter by looking that up ourselves?)
# add_headers: additional livestatus headers to add
# only_sites: list of sites the query is limited to
# limit: maximum number of data rows to query
def query_data(datasource, columns, add_headers, filters_string, only_sites = [], limit = None):
    if "add_columns" in datasource.keys():
        add_columns = datasource["add_columns"]
    else:
        add_columns = ['']

    tablename = datasource["table"]
    add_headers += datasource.get("add_headers", "")
    merge_column = datasource.get("merge_by")
    if merge_column:
        columns = [merge_column] + columns

    # Most layouts need current state of object in order to
    # choose background color - even if no painter for state
    # is selected. Make sure those columns are fetched. This
    # must not be done for the table 'log' as it cannot correctly
    # distinguish between service_state and host_state
    if "log" not in datasource["infos"]:
        state_columns = []
        if "service" in datasource["infos"]:
            state_columns += [ "service_has_been_checked", "service_state" ]
        if "host" in datasource["infos"]:
            state_columns += [ "host_has_been_checked", "host_state" ]
        for c in state_columns:
            if c not in columns:
                columns.append(c)

    # Remove columns which are implicitely added by the datasource
    if add_columns:
        columns = [ c for c in columns if c not in add_columns ]

    query = "GET %s\n" % tablename
    query += "Columns: %s\n" % " ".join(columns)
    query += add_headers
    query += filters_string
    live.set_prepend_site(True)
    if limit != None:
        live.set_limit(limit + 1) # + 1: We need to know, if limit is exceeded

    if only_sites:
        live.set_only_sites(only_sites)
    data = live.query(query)
    live.set_only_sites(None)
    live.set_prepend_site(False)
    live.set_limit() # removes limit

    if merge_column:
        data = merge_data(data, columns)

    # convert lists-rows into dictionaries.
    # performance, but makes live much easier later.
    columns = ["site"] + columns + add_columns
    rows = [ dict(zip(columns, row)) for row in data ]

    return rows


# Merge all data rows with different sites but the same value
# in merge_column. We require that all column names are prefixed
# with the tablename. The column with the merge key is required
# to be the *second* column (right after the site column)
def merge_data(data, columns):
    merged = {}
    mergefuncs = [lambda a,b: ""] # site column is not merged

    def worst_service_state(a, b):
        if a == 2 or b == 2:
            return 2
        else:
            return max(a, b)

    def worst_host_state(a, b):
        if a == 1 or b == 1:
            return 1
        else:
            return max(a, b)

    for c in columns:
        tablename, col = c.split("_", 1)
        if col.startswith("num_") or col.startswith("members"):
            mergefunc = lambda a,b: a+b
        elif col.startswith("worst_service"):
            return worst_service_state
        elif col.startswith("worst_host"):
            return worst_host_state
        else:
            mergefunc = lambda a,b: a
        mergefuncs.append(mergefunc)

    for row in data:
        mergekey = row[1]
        if mergekey in merged:
            oldrow = merged[mergekey]
            merged[mergekey] = [ f(a,b) for f,a,b in zip(mergefuncs, oldrow, row) ]
        else:
            merged[mergekey] = row

    # return all rows sorted according to merge key
    mergekeys = merged.keys()
    mergekeys.sort()
    return [ merged[k] for k in mergekeys ]


