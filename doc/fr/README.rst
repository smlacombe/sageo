=====
Sageo
=====

Présentation
-------- 

Sageo est une réécriture de l'interface web `check_mk_ multisite
<http://mathias-kettner.de/checkmk_multisite.html>`_.

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

Application globale

- Tests

Captures d'écran
-------- 

La vue « tous les hosts »

.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/allhosts.png 
    :alt: Vue all hosts 
    :align: center

La vue « tous les services »

.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/allservices.png 
    :alt: Vue all services
    :align: center

L'édition de vue

.. image:: https://raw.github.com/smlacombe/sageo/master/doc/screenshots/edit_view.png 
    :alt: Édition de vue
    :align: center

La liste des vues disponibles 

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

Création d'un environnement virtuel python
.. code-block:: bash

    $ virtualenv env
    $ . env/bin/activate

Télécharger le code source du dépôt GIT
.. code-block:: bash

    $ git clone https://github.com/smlacombe/sageo.git
    $ cd sageo
    $ pip install -r requirements.txt
    $ python db_create.py

Installer les modules python avec pip
.. code-block:: bash

    $ pip install -r requirements.txt

Créer la base de données
.. code-block:: bash
    $ python db_create.py

Configuration
-------------

Ajouter l'adresse de votre broker

.. code-block:: bash

    $ vim config.py

Compiler les fichiers LESS (CSS)
-------------------------------- 

Vous devant avant tout installer le compilateur LESS (Commande LESSC)

Pour les distributions basées sur Debian:

.. code-block:: bash

    $ apt-get install lessc

Compiler les fichiers LESS

.. code-block:: bash

    $ cd app/static/css
    $ lessc less/main.less main.css

Démarrer le serveur
------------------- 

.. code-block:: bash
    $ python run.py

Ouvrir le navigateur et aller à: http://127.0.0.1:5000

Le nom d'utilisateur et le mot de passe par défaut est "admin" et "jobs" respectivement.

=======================
Documentation technique
=======================

Ajout de colonnes pour les vues
-------------------------------

1. Aller dans le dossier 'columns'

.. code-block:: bash
    $ cd app/model/columns 

Vous allez voir plusieurs classes « column_painter » et un un module « builtin.py ».
Un column painter sert à l'obtention d'une donnée lisible pour l'utilisateur à partir des données brutes provenant de Livestatus. Cet objet stocke également différentes propriétés pour une colonne donnée.

Regardez s'il existe déjà une classe « column painter » implémentant le type de colonne que vous désirez ajouter. Un « column painter » peut-être générique pour plusieurs colonnes de même type i.e host_state et service_state sont des états et utilise le même « column painter » ColumnPainterState. Plus la classe « column painter » est générique, plus il devrait y avoir des paramètres passé au constructeur de la classe.

Pour implémenter un « column painter » regarder la structure de la classe de base ColumnPainter. Elle spécifie qu'il faut implémenter dans la classe concrète, la fonction get_readable(row). Row représente le dictionnaire contenant les colonnes brutes de livestatus qui ont été demandées.

Pour les colonnes qui ne nécessite pas de conversion pour être lisible par l'utilisateur comme le host_name par exemple, il faut utiliser le « painter » ColumnPainterRaw.

2. Aller dans builtin.py

.. code-block:: bash
    $ vi columns/builtin.py 

3. Dans l'entête du fichier, importer la classe « column painter » si ce n'est pas déjà fait.

ex:

.. code-block:: python
    from .column_painter_raw import ColumnPainterRaw

4. Déclarez en constante, le nom de la colonne.

ex:

.. code-block:: python
    COL_HOST_NAME = 'host_name'

5. Stockez le painter dans le dictionnaire « painters »

ex:

.. code-block:: python
    painters[COL_HOST_NAME] = ColumnPainterRaw(COL_HOST_NAME, _(u'Host name'), _(u'Host name'), ['hosts', 'services']) 

Redémarrer le serveur et les nouvelles colonnes apparaîtront dans les vues ayant un datasource relié.

Ajout de filtres pour les vues
---------------------------------

La liste des filtres n'est pas encore complète. Nous vous encourageons à nous soummettre des filtres.

1. Aller dans le dossier 'filters'

.. code-block:: bash
    $ cd app/model/filters

Vous allez voir plusieurs classes « filter » et un un module « builtin.py ». Un filtre définit une fonction « filter » permettant de retourner le filtre texte pour livestatus correspondant à la requête de filtrage. Un filtre définit aussi la fonction « get_col_def » retournant la définition des colonnes pour la base de données.

Implémenter une classe de filtre si les classes présentes ne suffisent pas.

2. Aller dans builtin.py

.. code-block:: bash
    $ vi filter/builtin.py 

3. Dans l'entête du fichier, importer la classe « column painter » si ce n'est pas déjà fait.

ex:

.. code-block:: python
    from app.model.filters.filter_text import FilterText

4. Déclarez en constante, le nom du filtre.

ex:

.. code-block:: pytho
    FILTER_HOSTREGEX = 'host_regex'

5. Stockez le filtre dans le dictionnaire « filters »

ex:

.. code-block:: python
    filters[FILTER_HOSTREGEX] = FilterText(FILTER_HOSTREGEX, _("Hostname"), _("Search field allowing regular expressions and partial matches"), ["host_name"], OP_TILDE)

6. S'assurer d'avoir la fonction d'affichage nécessaire pour le type du filtre.  

.. code-block:: bash
    vim app/templates/views/filter_fields.html

7. S'assurer que les templates puissent afficher correctement les filtres.
Étant donné la généricité des filtres lors de leur utilisation, ce sont les types des champs qui définissent comment les filtres seront affiché dans l'interface web.

.. code-block:: bash
    $ vim app/templates/lib/views.html


Redémarrer le serveur et les nouveaux filtres apparaîtront dans les vues ayant un datasource relié.

Ajout de snapin
---------------

Un snapin est constitué d'un dossier avec un fichier python ayant le même nom à l'intérieur. Ce fichier définit une classe héritant de la classe de base « SnapinBase ». Il définit une méthode context permettant de faire un traitement et de retourner un objet pour son utilisation dans le template du snapin. Le template est à l'intérieur d'un dossier « template ». Il y un fichier html ayant le même préfixe que le fichier python, et un fichier styles.css. Pour qu'un spanin soit multilingue, il faut un dossier translations à l'intérieur du dossier du snapin. Il s'agit ensuite de la même structure que les fichiers Babel. Dans la classe du snapin, il faut définir comme dans le SnapinAbout, un code pour aller chercher les traduction selon la langue actuelle.

Voici la hiéarchie type d'un snapin:

- SnapinExemple
    - __init__.py
    - SnapinExemple.py
    - template
        - SnapinExemple.html
        - style.css (facultatif)
    - translations
        - ...

Au redémarrage de l'application, les snapins sont automatiquement pris en compte.

