import glob
import re
"""Lists all of the importable plugins"""
#TODO: find a way to glob correctly whatever the path sageo is launched
snapins = glob.glob('app/snapins/snapin_*.py')
snapins = list([re.match('app/snapins/(snapin_.*).py', x).groups()[0] for x in snapins])
__all__ = snapins
