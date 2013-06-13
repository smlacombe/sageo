import glob
import re
"""Lists all of the importable plugins"""
import ipdb;ipdb.set_trace()
#TODO: find a way to glob correctly whatever the path sageo is launched
snapins = glob.glob('app/snapins/*.py')
snapins = list([re.match('app/snapins/(.*).py', x).groups()[0] for x in snapins])
snapins.remove('__init__')
__all__ = snapins
