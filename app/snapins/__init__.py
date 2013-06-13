import glob
import re
"""Lists all of the importable plugins"""

snapins = glob.glob('snapins/*.py')
snapins = list([re.match('snapins/(.*).py', x).groups()[0] for x in snapins])
snapins.remove('__init__')
__all__ = snapins
