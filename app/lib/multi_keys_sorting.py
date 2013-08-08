from operator import itemgetter
def multikeysort(items, columns, functions={}, getter=itemgetter):
    """Sort a list of dictionary objects or objects by multiple keys bidirectionally.

    Keyword Arguments:
    items -- A list of dictionary objects or objects
    columns -- A list of column names to sort by. Use -column to sort in descending order
    functions -- A Dictionary of Column Name -> Functions to normalize or process each column value
    getter -- Default "getter" if column function does not exist
              operator.itemgetter for Dictionaries
              operator.attrgetter for Objects
    """
    comparers = []
    for col in columns:
        column = col[1:] if col.startswith('-') else col
        if not column in functions:
            functions[column] = getter(column)
        comparers.append((functions[column], 1 if column == col else -1))

    def comparer(left, right):
        for func, polarity in comparers:
            result = cmp(func(left), func(right))
            if result:
                return polarity * result
        else:
            return 0
    return items.sort(cmp=comparer)

def compose(inner_func, *outer_funcs):
     """Compose multiple unary functions together into a single unary function"""
     if not outer_funcs:
         return inner_func
     outer_func = compose(*outer_funcs)
     return lambda *args, **kwargs: outer_func(inner_func(*args, **kwargs))
