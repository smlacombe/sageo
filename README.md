Sageo
=====

Presentation
------------
Sageo is a rewriting of [check_mk multisite](http://mathias-kettner.de/checkmk_multisite.html) web GUI. The Sageo project started with the idea of having a monitoring web GUI that is: 

- Able to browse many sites at a time
- Easy to maintain 
- Using up to date technologies 
- Lightweight

Sageo reimplement the view customization feature of check_mk. 

Sageo offers many advantages over by check_mk multisite:

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
------------
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
------------
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

Installation
------------

# Dependencies
<pre><code>sudo aptitude install python-virtualenv</code></pre>

# Installation
<pre><code>virtualenv env
. env/bin/activate
git clone https://github.com/smlacombe/sageo.git
cd sageo
pip install -r requirements.txt
python db_create.py
</code></pre>


# Configuration
Add your broker address
<pre><code>vim config.py
</code></pre>

# Compile LESS files (CSS)
You need first to install LESS compiler (LESSC command)

Debian based:
<pre><code>
apt-get install lessc
</pre></code>

Compile LESS files
<pre><code>
cd app/static/css
lessc less/main.less main.css
</code></pre>

# Run server
Launch server
<pre><code>python run.py
</code></pre>
Go to : http://127.0.0.1:5000
The default username and the default password is 'admin' and 'jobs' respectively.
