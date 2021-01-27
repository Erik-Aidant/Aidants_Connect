# Aidants Connect

[![CircleCI](https://circleci.com/gh/betagouv/Aidants_Connect/tree/master.svg?style=svg)](https://circleci.com/gh/betagouv/Aidants_Connect/tree/master)

Aidants Connect est une application web qui propose à des aidants les fonctionnalités suivantes :
- créer un mandat de connexion via [FranceConnect](https://franceconnect.gouv.fr/) avec un ou plusieurs usagers sur un périmètre et une durée définis ;
- connecter via FranceConnect un usager dans les conditions des mandats créés ;
- accéder à des ressources sur l'accompagnement des usagers ;
- accéder à un suivi de ses mandats.

## Sommaire
1. Pile technique
2. Installer et lancer l'application
   2.1. Installer la base de données (pour Mac OSX)
   2.2. Installer l'application
   2.3. Peupler la base de données
    2.3.1 Installation en local pour test : utiliser les _fixtures_
    2.3.2 Installation sur un serveur : Créer un _superuser_
   2.4. Lancer l'application
   2.5. Se connecter à l'application : authentification à double facteur (2FA)
3. Lancer les tests
4. Contribuer à l'application
5. Annexes
  5.1. Documentation de FranceConnect
  5.2. Ré-initialiser la base de données
  5.3. Purger les connexions expirées
  5.4. Utiliser le Makefile
  5.5. Calcul de `HASH_FC_AS_FI_SECRET` à partir de la valeur de `FC_AS_FI_SECRET` 
   
## Pile technique

- Python 3.7
- Django 3.0
- PostgreSQL

## Installer et lancer l'application

### Installer la base de données (pour Mac OSX)

Utilisez votre gestionnaire de paquets préféré pour installer la base.
L'exemple qui suit emploie le gestionnaire [Homebrew](https://brew.sh) via la commande `brew`.

Dans un terminal, installez [PostgreSQL](https://www.postgresql.org) :

```sh
brew install postgresql
```

Démarrez le service postgresql :

```sh
brew services start postgresql
```

> Ceci démarre le serveur de la base de données et active sa réexécution au login.

Dans le cas où ce serait votre première utilisation de PostgreSQL, créez une base d'essai à votre nom :

```sh
createdb `whoami`
```

Puis, démarrez l'invite de commande PostgreSQL :

```sh
psql
```

Vous pouvez dès à présent visualiser :
* la liste des bases de données existantes avec cette commande PostgreSQL `\list`
* la liste des roles existants avec `\du`

Ajoutez une base `aidants_connect` appartenant au nouvel utilisateur `aidants_connect_team` en poursuivant dans l'invite de commmande PostgreSQL :

```sql
CREATE USER aidants_connect_team;
CREATE DATABASE aidants_connect OWNER aidants_connect_team;
ALTER USER aidants_connect_team CREATEDB;
```

:tada: La base de donnée `aidants_connect` est installée. Vous pouvez la voir et quitter l'invite de commande avec :

```sql
\list
\q
```

### Installer l'application

Dans votre répertoire de travail, créez et activez un environnement virtuel :

```shell
virtualenv venv
source venv/bin/activate
```

Installez les dépendances :

```shell
pip install -r requirements.txt
```

Si la commande précédente déclenche le message d'erreur suivant `ld: library not found for -lssl`, essayez :

```shell
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/
```

Dupliquez le fichier `.env.example` à la racine du projet en tant que `.env` et ajoutez vos informations :
- Les champs obligatoires sont indiqués par le préfixe `<insert_`
- Les informations `FC_AS_FS` et `FC_AS_FI` sont à récupérer via des [habilitations FranceConnect](https://franceconnect.gouv.fr/partenaires)
- Vous allez devoir calculer la valeur `HASH_FC_AS_FI_SECRET` à partir de la valeur de `FC_AS_FI_SECRET`  pour cela voir dans les annexes [la procédure](#calcul-de-hash_fc_as_fi_secret-à-partir-de-la-valeur-de-fc_as_fi_secret)
- Les valeurs de sécurité sont issues de https://docs.djangoproject.com/fr/2.2/topics/security/ et de https://www.youtube.com/watch?v=gvQW1vVNohg

Créez un répertoire `staticfiles` à la racine du projet :

```shell
mkdir staticfiles
```

Appliquez les migrations de la base de données :

```shell
python manage.py migrate
```

Créez un _superuser_ :

```shell
python manage.py createsuperuser --username <insert_admin_name>
```

Adjoignez-lui une `Organisation` :

```
python manage.py shell
from aidants_connect_web.models import Aidant, Organisation
a = Aidant.objects.get(pk=1)
a.organisation = Organisation.objects.create(name=<insert_organisation_name>)
a.save()
exit()
```

### Lancer les tests

Si vous ne les avez pas, installez les éléments suivants :
- Navigateur Firefox en [téléchargement](https://www.mozilla.org/fr/firefox/download/thanks/)
- [Gecko driver](https://github.com/mozilla/geckodriver/releases) avec cette commande :
    ```shell
    brew install geckodriver
    ```
**_NOTE:_** Si vous êtes sous linux, vous pouvez télécharger [ici](https://github.com/mozilla/geckodriver/releases) la dernière
version du driver et déposer le fichier  `geckodriver` dans `VOTRE_VENV/bin` (ou dans `/usr/local/bin` si vous voulez
donner un accès global au driver). 

Avant de lancer les tests il faudra augmenter la valeur de la variable d'environnement `ACTIVITY_CHECK_THRESHOLD` qui 
est par défaut à 0 (ce qui fera échouer plein de tests).

Puis lancez les commandes suivantes pour vérifier le style du code source et exécuter les tests de l'application :

```shell
flake8
python manage.py test
```

Les tests fonctionnels sont lancés sur `http://localhost:3000`.
Il faut s'assurer que rien d'autre n'occupe ce port pendant leur exécution.

Par défaut, les tests d'intégration sont lancés en mode _headless_, c'est-à-dire sans ouverture de fenêtre de navigateur. Si vous souhaitez modifier ce comportement, vous pouvez modifier la valeur de la variable d'environnement `HEADLESS_FUNCTIONAL_TESTS` dans votre fichier `.env`.

Dans de rares cas (comportement observé à ce jour sur une seule machine de dev), les tests d'intégration échouent car _la première connexion_ à une URL via l'API Selenium plante de manière inexpliquée. Un contournement empirique a été mis en place ; si vous rencontrez ce problème vous pouvez l'activer en passant à `True` la variable d'environnement `BYPASS_FIRST_LIVESERVER_CONNECTION` dans votre fichier `.env`.

### Lancer l'application

Pour lancer l'application sur le port `3000` :

```shell
python manage.py runserver 3000
```

L'application sera disponible à l'URL `http://localhost:3000/`

### Se connecter à l'application : authentification à double facteur (2FA)

Pour pouvoir vous connecter à votre instance locale, il faut apparier à votre `superuser` un dispositif TOTP (`TOTP device`).

Pour cela, commencez par lui adjoindre un [jeton OTP](https://fr.wikipedia.org/wiki/Mot_de_passe_%C3%A0_usage_unique) [statique](https://django-otp-official.readthedocs.io/en/stable/overview.html#module-django_otp.plugins.otp_static) :

```shell
python manage.py addstatictoken <insert_admin_name> -t <insert_6_numbers>
```

Le jeton généré vous permet de vous connecter une seule fois à l'interface d'administration Django, disponible par défaut à l'URL `http://localhost:3000/admin/` (sauf si vous avez spécifié une autre URL dans la variable d'environment `ADMIN_URL`).
En cas de problème, pas d'inquiétude : vous pouvez répéter la procédure précédente autant que nécessaire :)

Une fois connecté à l'admin, voici les étapes pour ajouter un dispositif TOTP à votre `superuser` :
1. cliquez sur _TOTP devices_
2. Cliquez sur le bouton _Ajouter TOTP device +_
3. Choisissez votre `superuser` grâce à l'icône "loupe" située à côté du champ _User_
4. Saisissez un nom pour votre dispositif TOTP (par exemple : _Mon téléphone_) dans le champ _Name_
5. Cliquez ensuite sur _Enregistrer et continuer les modifications_ tout en bas du formulaire
6. Une fois l'enregistrement effectué, l'écran devrait se rafraîchir et vous proposer un lien vers un [QR Code](https://fr.wikipedia.org/wiki/Code_QR)
7. Vous pouvez à présent scanner celui-ci dans une application TOTP telle que [Authy](https://authy.com/) ou [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2) pour utiliser l'authentification à double facteur dans votre environnement local.

## Contribuer à l'application

Il faut d'abord avoir correctement installé l'application.

Installez les _git hooks_ :
```
pre-commit install
```

## Annexes

### Documentation de FranceConnect

- Fournisseur d'Identité (FI): [ici](https://partenaires.franceconnect.gouv.fr/fcp/fournisseur-identite)
- Fournisseur de Service (FS): [ici](https://partenaires.franceconnect.gouv.fr/fcp/fournisseur-service)

### Ré-initialiser la base de données

Si vous avez des données existantes, vous pouvez d'abord les sauvegarder :

```shell
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
```

Puis il vous faudra recréer la base de donnée PostgreSQL :

- Dans le shell :

    ```shell
    psql
    ```

- Puis, dans l'invite de commande `psql` :

    ```sql
    DROP DATABASE aidants_connect;
    CREATE DATABASE aidants_connect OWNER aidants_connect_team;
    ALTER USER aidants_connect_team CREATEDB;
    \q
    ```

Ensuite, de retour dans le _shell_, pour lancer les migrations :

```shell
python manage.py migrate
```

Enfin, chargez les données :

- Soit des données sauvegardées précédement :

    ```shell
    python manage.py loaddata db.json
    ```

- Soit des données de test qui créent aussi un _superuser_ rattaché à une `Organisation` `BetaGouv`:
    * identifiant : `admin@email.com`;
    * mot de passe : `admin`;
    * Static OTP : `111111`.

    ```shell
    python manage.py loaddata admin.json
    python manage.py loaddata usager_autorisation.json
    ```

- Soit repartir de zéro en recréant un _superuser_ (plus de détails dans la section [Installer l'application](#installer-lapplication)) :

    ```shell
    python manage.py createsuperuser
    ```
  
### Purger les connexions expirées

Les objets Django de type `Connection` repésentent une forme de cache pendant l'établissement de la connexion FranceConnect.
À ce titre, ils contiennent des données personnelles et doivent donc être purgés régulièrement pour respecter nos engagements en la matière.
Pour ce faire, il suffit d'exécuter ou de planifier la commande suivante :

```shell
python manage.py delete_expired_connections
```

### Utiliser le Makefile

Pour simplifier le lancement de certaines commandes, un Makefile est disponible. Exemples de commandes :

```shell
make shell
make test
make migrate
```

### Calcul de `HASH_FC_AS_FI_SECRET` à partir de la valeur de `FC_AS_FI_SECRET`    
Il faut utiliser `generate_sha256_hash`.

```python
from aidants_connect_web.utilities import generate_sha256_hash
generate_sha256_hash("VALUE_FC_AS_FI_SECRET".encode("utf-8"))
```
