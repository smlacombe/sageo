=====
Sageo
=====

**Table of contents**

.. contents::
    :local:
    :backlinks: none

Presentation
************

Sageo (prononced Sah-gay-oh) is a rewriting of `check_mk_ multisite
<http://mathias-kettner.de/checkmk_multisite.html>`_ web GUI. 

The Sageo project started with the idea of having a monitoring web GUI that is: 

- Able to browse many sites at a time
- Easy to maintain 
- Builded with up to date technologies 
- Lightweight

Sageo reimplement the view customization feature of check_mk. 

Sageo offers these advantages over by check_mk multisite:

- Sageo doesn't use the deprecated apache modules mod_python.
- Sageo is MVC oriented, that means the content and the business logic is seperated from presentation.

Sageo is compatible with all monitoring plateforms providing a livestatus interropability, like Icinga, Nagios, Shinken, etc. 

The main technologies used are:

- Flask web framework
- MK Livestatus
- Twitter Bootstrap
- LESS
- Babel
- SQL ALCHEMY
- WTFORMS-ALCHEMY

Features
--------

Views

- View editing  
- Backend multi-columns sorting
- Frontend multi-columns sorting
- Multi-columns grouping
- Backend filters
- Frontend filters
- Columns order customizing by drag & drop
- Layout column number customization

Views templates

- Table aspect

Snapins

- Snapin development structure
- Snapin localizable
- Snapin presentation customized by drag & drop
- Tactical overview ported

Users

- Languages preferences

Global application

- Display easily external content with a framed mode.
- Localizable 
- Easily web forms creation according to the DB model
- Content and logic separated from presentation

Upcoming features
-----------------
Views

- Views rights management
- Columns linking
- Results pagination
- Commands execution on objects

Views templates

- Single dataset

Snapins

- Snapin preferences saving

Users

- User privileges
- Login configuration

Global application

- Tests


Screenshots
------------
The view "all hosts"

.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/allhosts.png 
    :alt: Vue all hosts 
    :align: center

The view "all services"

.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/allservices.png 
    :alt: Vue all services
    :align: center

View editing

.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/edit_view.png 
    :alt: Édition de vue
    :align: center

Available views list

.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/views_list.png 
    :alt: Liste des vues disponibles
    :align: center

Start-up
********

Dependencies
------------

.. code-block:: bash

    $ sudo aptitude install python-virtualenv

Installation
------------

Create you virtual environnement

.. code-block:: bash

    $ virtualenv env
    $ . env/bin/activate

Download the GIT repository

.. code-block:: bash

    $ git clone https://github.com/smlacombe/sageo.git
    $ cd sageo
    $ pip install -r requirements.txt

Install python modules with pip

.. code-block:: bash

    $ pip install -r requirements.txt

Create the database

.. code-block:: bash

    $ python db_create.py

Configuration
-------------

Add your broker adress

.. code-block:: bash

    $ vim config.py

Example:

.. code-block:: python

    SITES = {
      "Site 1": {
         "alias":          "Shinken demo 2",
         "socket":         "tcp:192.168.40.43:50001",
         "url_prefix":     "http://192.168.40.43",
       },
      "Site 2": {
         "alias":          "Shinken demo",
         "socket":         "tcp:192.168.57.43:50000",
         "url_prefix":     "http://192.168.57.43",
       },

    }

Compile the LESS files
-------------------------------- 

You need first to install the LESS compiler (LESSC).

For Debian based distribution:

.. code-block:: bash

    $ apt-get install node-less


Compiling stuff

.. code-block:: bash

    $ cd app/static/css
    $ lessc less/main.less main.css


Start the server
------------------- 

.. code-block:: bash

    $ python run.py

Open a browser et go to: http://127.0.0.1:5000

The default username and the default password is 'admin' and 'jobs' respectively.


Technical documentation
***********************

Adding columns for views
-------------------------------

Go to the folder "column"

.. code-block:: bash

    $ cd app/model/columns 


You will see several classes named with the prefix "column_painter" and a "builtin.py" module.
A column painter used to obtain a readable data to the user from the raw data from livestatus queries results. This object also stores various properties for a given column.

Look if there is already a "painter column" class that implements the type of column that you want to add. A "column painter" may be generic for multiple columns of the same type. For instance, host_state and service_state are both states and uses the same "column painter" ColumnPainterState. More "column painter" class is generic, there should be more of the parameters passed to the constructor of the class.

To implement a "painter column", look at the structure of the base class ColumnPainter. It specifies that it must be implemented in the concrete class, the (row) get_readable function. Row is the dictionary containing the raw livestatus columns that have been requested.

For columns that does not require conversion to be readable by the user like the host_name, use the "painter" ColumnPainterRaw.

Go to builtin.py

.. code-block:: bash

    $ vi columns/builtin.py

In the file header, import the class "column painter" if it is not already done.

ex:

.. code-block:: python

    from .column_painter_raw import ColumnPainterRaw

Declare as a constant, the column name.

ex:

.. code-block:: python

    COL_HOST_NAME = 'host_name'

Store the "painter" in the "painters" dictionnary.

ex:

.. code-block:: python

    painters[COL_HOST_NAME] = ColumnPainterRaw(COL_HOST_NAME, _(u'Host name'), _(u'Host name'), ['hosts', 'services'])


Restart the server and the new columns will appears in the view related to it datasource.

Adding filters for views
---------------------------------

The filters list is not complete yet. We invite you to sumbit some filters.

Go to the folder "filters".

.. code-block:: bash

    $ cd app/model/filters


You will see several "filter" and a "builtin.py" module classes. A filter defines a "filter" function to return the text filter for livestatus matching the query filter. A filter also defines "get_col_def" function returning the column definition for the database.

Implement a filter class if these classes are not enough.

Go to builtin.py

.. code-block:: bash

    $ vi filter/builtin.py

In the file head, import the filter class if it is not already done.


ex:

.. code-block:: python

    from app.model.filters.filter_text import FilterText

Declare as constant, the filter name.

.. code-block:: python

    FILTER_HOSTREGEX = 'host_regex'

Store the filter into the filters dictionnary.

ex:

.. code-block:: python

    filters[FILTER_HOSTREGEX] = FilterText(FILTER_HOSTREGEX, _("Hostname"), _("Search field allowing regular expressions and partial matches"), ["host_name"], OP_TILDE)

Be sure having the required display function for the filter type.

.. code-block:: bash

    vim app/templates/views/filter_fields.html

Ensure that the templates can show filters correctly.
Filters are generics, so it is the filters fields types that will determinate how filter will be displayed.

.. code-block:: bash

    $ vim app/templates/lib/views.html

Migrating the database, that will add new filters field in the filters table.
Go to the projet root directory

.. code-block:: bash

    $ python db_migrate.py 

Restart the server and the new filters will appears in the datasource related views.

Adding snapins
-------------

A snapin consists of a folder with a python file with the same name inside. This file defines a class that inherits from the base class "SnapinBase." It defines a context method to do the processing and return an object to its use in the template of the snapin.

The template is within a "template" folder. There is an html file with the same prefix as the python file and styles.css file.

To have a multilingual snapin, it takes a translation folter within the snapin file folder. It is then the same structure as the Babel files. Howver, in snapin classn, you must define like in the SnapinAbout, a litle code to get the translation in the current language.

Restart the application, the new snapins will be automatically taken into account.

This is the common hiearchy of snapin:

- SnapinExample
    - __init__.py
    - SnapinExample.py
    - template
        - SnapinExample.html
        - style.css (facultatif)
    - translations
        - ...

Helping us translate Sageo
--------------------------

Sageo is multilanguages with the help of `Babel
<http://babel.pocoo.org>`_ and of FlaskBabelEx, a fork of `FlaskBabel
<http://pythonhosted.org/Flask-Babel>`_.

To contribute to translations, please look the `Flask-Babel traduction documentation
<http://pythonhosted.org/Flask-Babel/#translating-applications>`_.

We suggest you the software `Poedit
<http://www.poedit.net>`_ to translate. 

