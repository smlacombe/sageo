=====
Sageo
=====

Presentation
-------- 

Sageo est une réécriture de l'interface web `check_mk_ multisite
<http://mathias-kettner.de/checkmk_multisite.html/>`_.

Le projet Sageo est né avec l'idée d'avoir une interface web de supervision qui est à la fois: 

- Capable de gérer plusieurs sites à la fois
- Facile à maintenir
- Constitué de technologies à jour
- Léger

Un des points forts de Sageo est sa réimplémentation du système de vues de check_mk multisite.

Sageo offre de nombreux avantages par rapport à check_mk multisite:

- Pas d'utilisation du module apache déprécié 'mod_python'.
- Orienté MVC, ce qui permet de découpler le contenu et la logique d'affaire de la présentation.

Sageo est compatible avec tous les plateformes de supervision fournissant une interopérabilité avec MK livestatus comme Icinga, Nagios et Shinken.

Les principales technologies utilisées sont:

- Flask
- MK Livestatus
- Twitter Bootstrap
- LESS
- Babel
- SQL ALCHEMY
- WTFORMS-ALCHEMY

Fonctionnalités
-------- 

Vues

- Édition de vues
- Tri multi-colonnes dans l'interface et dans l'édition de la vue
- Regroupement multi-colonnes 
- Filtres dans l'interface et dans l'édition de la vue
- Changement de l'ordre des colonnes par un glisser & déposer
- Paramétrisation de l'affichage des vues avec un nombre de colonnes modulable.

Apparence des vues

- Apparence de table

Snapins

- Modularité
- Facile d'ajouter un snapin
- Snapin traduisible
- Snapin facilement déplaçable dans l'interface avec un glisser & déposer
- Snapin 'Tactical overview' porté

Utilisateurs

- Langue préférée

Application générale

- Affiche facilement du contenu externe grâce à un mode "frame"
- Internationalisation et localisation
- Facilité de créer des formulaires web à partir du modèle de la BD 

Fonctionnalités à venir
-------- 

Vues

- Gestion des droits
- Lien des columns (pour se déplacer entre vues)
- Pagination des résultats des vues
- Exécution de commandes livestatus sur les objets supervisés

Apparence des vues

- Objet simple (single dataset)

Snapins

- Sauvegarde des préférences des snapins (position, liste des snapins utilisée, etc.)

Utilisateurs

- Privilèges des utilisateurs
- Changement du login et des options personnelles

Captures d'écran
-------- 
.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/allhosts.png 
    :alt: Vue all hosts 
    :align: center

.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/allservices.png 
    :alt: Vue all services
    :align: center

.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/edit_view.png 
    :alt: Édition de vue
    :align: center

.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/views_list.png 
    :alt: Liste des vues disponibles
    :align: center

=====
Mise en route
=====

Dépendances
-------- 

.. code-block:: bash

    $ sudo aptitude install python-virtualenv 

Installation
-------- 

.. code-block:: bash

    $ virtualenv env
    $ . env/bin/activate
    $ git clone https://github.com/smlacombe/sageo.git
    $ cd sageo
    $ pip install -r requirements.txt
    $ python db_create.py

Configuration
-------- 

Ajouter l'adresse de votre broker

.. code-block:: bash

    $ vim config.py

Compiler les fichiers LESS (CSS)
-------- 

Vous devant avant tout installer le compilateur LESS (Commande LESSC)

Pour les distributions basées sur Debian:

.. code-block:: bash

    $ apt-get install lessc

Compiler les fichiers LESS

.. code-block:: bash

    $ cd app/static/css
    $ lessc less/main.less main.css

Démarrer le serveur
-------- 

.. code-block:: bash
    $ python run.py

Ouvrir le navigateur et aller à: http://127.0.0.1:5000
Le nom d'utilisateur et le mot de passe par défaut est "admin" et "jobs" respectivement.

=======================
Documentation technique
=======================

Ajout de colonnes
-----------------

cd app/model/columns
