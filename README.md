sageo
=====

A rewriting of check_mk multisite web interface with the Flask web framework
The technologies used are:
- Twitter Bootstrap for CSS styles
- Python Flask web framework
- Babel for translations
- MK Livestatus


Installation
------------

# Dependencies
<pre><code>
sudo aptitude install python-virtualenv
</code></pre>

# Installation
<pre><code>
virtualenv env
. env/bin/activate
git clone https://github.com/smlacombe/sageo.git
cd sageo
pip install -r requirements.txt
python db_create.py
</code></pre>


# Configuration
Add your broker address
<pre><code>
vim config.py
</code></pre>

# Run server
Launch server
<pre><code>
python run.py
</code></pre>

Go to : http://127.0.0.1:5000
