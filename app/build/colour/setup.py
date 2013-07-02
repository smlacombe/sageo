from setuptools import setup, find_packages


long_description = '\n\n'.join([open('README.rst').read(),
                                open('CHANGELOG.rst').read(),
                                open('TODO.rst').read()])

from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    name='colour',
    version='0.0.2',
    description='converts and manipulates various color representation (HSL, RVB, web, X11, ...)',
    long_description=long_description,
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development",
        "Topic :: Software Development :: Version Control",
        "Programming Language :: Python :: 2.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='color convertion',
    author='Valentin Lab',
    author_email='valentin.lab@kalysto.org',
    url='http://github.com/vaab/colour',
    license='GPL License',
#    package_data={'': ['rgb.txt']},
#    include_package_data=True,
    py_modules=['colour'],
    data_files=['rgb.txt'],
    namespace_packages=[],
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
    entry_points="",
)
