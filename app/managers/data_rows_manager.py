from app.db_model.view import View
from app.db_model.base import db_session
from app.db_model.viewColumn import ViewColumn
from app.lib import livestatus_query
from app.lib.datasources import multisite_datasources as datasources
from app.lib.multi_keys_sorting import compose, multikeysort
from app.managers.filters_manager import FiltersManager
from app.managers.view_manager import ViewManager
from app.model.columns.builtin import painters
import copy
from operator import itemgetter, methodcaller

class DataRowsManager():
    """ A sort of proxy that facilitate gathering data from LiveStatus without knowing implementation details. """
    def __init__(self):
        self.__view_manager = None
        self.__filters_manager = None
    '''
    Set the view with the link_name. If a view is found, return true, else return false.
    '''
    def set_view(self, link_name):
        self.__view_manager = ViewManager()
        if self.__view_manager.set_view(link_name):
            self.__filters_manager = FiltersManager()
            self.update_filters()
            return True
        else:
            return False

    def update_filters(self):
        self.__filters_manager.set_filters(self.__view_manager.get_filters())

    def get_group_columns_list(self):
        groupers = self.__view_manager.get_groupers()
        group_list = []
        if groupers:
            for group in groupers:
                group_list.append(group.column)
        return group_list

    def get_rows(self):
        """ get rows corresponding to the query builded with the view and its options """
        # prepare basic parameter datasource and columns_name
        datasource = datasources[self.__view_manager.get_view().datasource]        
        columns_name = self.get_asked_columns_name()
        filters_string = self.__filters_manager.get_filter_query() 
        print '\nfilters: ' + filters_string
        rows = livestatus_query.get_rows(datasource, columns_name, filters_string)         

        if not rows == []:
            groupers = self.__view_manager.get_groupers()
            sort_list = []
            for grouper in groupers:
                sort_list.append((grouper.column,0))
            rows = self.group(rows, self.get_group_columns_list())  
            rows = sorted(list((k, v) for k,v in rows.items()))

            sorters = self.__view_manager.get_sorters()
            if sorters:
                sort_list = []
                for sorter in sorters:
                    sort_list.append((sorter.column,sorter.sorter_option))                
                rows = self.__sorted_rows(rows, sort_list)

            rows = self.__readable_rows(rows)
        return rows

    def get_sorters_dic(self):
        sorters = {}
        for sorter in self.__view_manager.get_sorters():
            sorters[sorter.column] = sorter.sorter_option 

        return sorters

    def __readable_rows(self, rows):
        rows_readable = rows 
        for group in rows_readable:
            for row in group[1]:
                for name, value in row.iteritems():
                    if name in painters.keys():
                        row[name] = painters[name].get_readable(row)
        return rows_readable
                
    def __sorted_rows(self, rows, sort_list):
        arguments = []
        callers = {}
        for sorter in sort_list:
            prefix = ''
            sort_order = sorter[1]
            column = sorter[0]
            if sort_order == '1':
                prefix = '-'
            arguments.append(prefix + column)
            if isinstance(rows[0][1][0][column], basestring): 
                get_lower = compose(itemgetter(column), methodcaller('lower'))
                callers[column] = get_lower

        for group in rows:
            multikeysort(group[1], arguments, callers)

        return rows

    def get_asked_columns_name(self):
        columns_names = []
        for column in self.__view_manager.get_columns(): columns_names.append(column.column)
        return columns_names

    def get_rows_count(self, rows):
        count = 0
        for group in rows:
            count = count + len(group[1])
        return count

    def get_asked_columns_title(self):
        columns_names = []
        for column in self.__view_manager.get_columns(): columns_names.append(painters[column.column].title)
        return columns_names
    
    def get_group_header(self, groupEnum):
        header = ""
        groups_list = self.get_group_columns_list() 
        for elem in groupEnum:
            curCol = groups_list[groupEnum.index(elem)]
            if not header == "":
                header = header + ', '
            readable_elem = painters[curCol].get_readable({curCol: elem})
            header = header + str(readable_elem)
        
        return header    

    def set_extra_filters(self, filters):
        self.__view_manager.set_filters(filters)
        self.update_filters()

    def get_filters_name(self):
        return self.__filters_manager.get_filters_name()
    
    def get_view(self):
        return self.__view_manager.get_view()

    def group(self, mylist, groups):
        #if not groups: return mylist
        def foo(mydict, row):
            key = tuple(map(lambda x: row[x], groups))
            if not key in mydict.keys():
                mydict[key] = []
            mydict[key].append(row)
            return mydict
        return reduce(foo, mylist, {})
