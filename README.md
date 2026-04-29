# Ecommerce Django Project

Projet e-commerce construit avec Django. L'application contient la gestion des produits, des categories, du panier, de l'authentification utilisateur et de la confirmation d'email.

## Fonctionnalites

- Liste des produits et detail d'un produit
- Liste des categories et detail d'une categorie
- Panier base sur la session
- Interface d'administration Django
- Inscription avec confirmation email avant creation du compte
- Connexion et deconnexion
- Profil utilisateur protege
- Modification du profil
- Changement de mot de passe avec templates personnalises
- Confirmation d'email pour l'inscription et pour le changement d'adresse email
- Base MySQL avec Docker Compose

## Structure du projet

```text
ecommerce_project-main/
|-- accounts/
|   |-- forms.py
|   |-- models.py
|   |-- urls.py
|   |-- views.py
|   `-- templates/
|       |-- accounts/
|       `-- registration/
|-- ecommerce/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|-- images/
|-- products/
|   |-- models.py
|   |-- urls.py
|   |-- views.py
|   |-- static/
|   `-- templates/
|-- venv/
|-- .env
|-- .env.example
|-- .gitignore
|-- db.sqlite3
|-- docker-compose.yaml
|-- manage.py
`-- README.md
```

## Prerequis

- Python 3
- Django
- Docker Desktop
- Driver MySQL pour Python (`mysqlclient`)

## Base de donnees MySQL

Le service MySQL est defini dans [docker-compose.yaml](/c:/Users/dell/Desktop/EMI/ecommerce_project-main/docker-compose.yaml:1).

Demarrer la base :

```powershell
docker compose up -d
```

Configuration par defaut :

- Base : `DB_ECOMMERCE`
- Utilisateur : `root`
- Mot de passe : `root`
- Host : `127.0.0.1`
- Port : `3306`

## Configuration Django

Le projet lit la configuration depuis les variables d'environnement et depuis le fichier [`.env`](</c:/Users/dell/Desktop/EMI/ecommerce_project-main/.env:1>).

Variables base de donnees :

```env
DB_NAME=DB_ECOMMERCE
DB_USER=root
DB_PASSWORD=root
DB_HOST=127.0.0.1
DB_PORT=3306
```

## Configuration email Gmail

Pour envoyer de vrais emails, remplissez [`.env`](</c:/Users/dell/Desktop/EMI/ecommerce_project-main/.env:1>) :

```env
EMAIL_HOST_USER=yourname@gmail.com
EMAIL_HOST_PASSWORD=your_google_app_password
DEFAULT_FROM_EMAIL=yourname@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
```

Notes :

- utilisez un mot de passe d'application Google, pas votre mot de passe Gmail normal
- si `EMAIL_HOST_USER` et `EMAIL_HOST_PASSWORD` sont vides, Django utilise le backend console et les emails s'affichent dans le terminal

## Installation

Activer l'environnement virtuel.

Sous `cmd` :

```cmd
venv\Scripts\activate.bat
```

Sous PowerShell :

```powershell
.\venv\Scripts\Activate.ps1
```

Installer les dependances si besoin :

```powershell
pip install django mysqlclient pillow
```

Si `mysqlclient` pose probleme sur Windows, il faudra installer les outils de build necessaires ou adapter le backend MySQL utilise.

## Lancement du projet

Appliquer les migrations :

```powershell
python manage.py migrate
```

Lancer le serveur :

```powershell
python manage.py runserver
```

Ouvrir ensuite :

```text
http://127.0.0.1:8000/
```

La racine `/` redirige automatiquement vers `/products/`.

## Authentification et comptes

L'application `accounts` ajoute :

- `/accounts/signup/` : inscription
- `/accounts/signup/pending/` : page d'attente avant confirmation
- `/accounts/signup/confirm/<token>/` : confirmation de creation du compte
- `/accounts/login/` : connexion
- `/accounts/logout/` : deconnexion
- `/accounts/profile/` : profil utilisateur
- `/accounts/profile/edit/` : modification du profil
- `/accounts/password_change/` : changement de mot de passe
- `/accounts/password_change/done/` : confirmation du changement
- `/accounts/confirm-email/<uidb64>/<token>/` : confirmation d'une adresse email modifiee

### Flux d'inscription

Le compte n'est pas cree immediatement.

1. L'utilisateur remplit le formulaire d'inscription
2. Une inscription en attente est creee
3. Un email de confirmation est envoye
4. Le compte Django reel est cree uniquement apres clic sur le lien
5. L'utilisateur est connecte automatiquement puis redirige vers la liste des produits

### Profil et email

Le profil permet :

- d'afficher les informations du compte
- de modifier `username`, `first_name`, `last_name` et `email`
- de voir si l'email est confirme
- de renvoyer un email de confirmation si necessaire

Si l'utilisateur change son adresse email, elle repasse en statut non confirme jusqu'a validation du nouveau lien.

## Application products

L'application `products` contient :

- modele `Category`
- modele `Product`
- liste des produits
- detail d'un produit
- liste des categories
- detail d'une categorie
- panier base sur la session

## Fichiers importants

- [ecommerce/settings.py](/c:/Users/dell/Desktop/EMI/ecommerce_project-main/ecommerce/settings.py:1) : configuration generale, base de donnees, email, auth
- [ecommerce/urls.py](/c:/Users/dell/Desktop/EMI/ecommerce_project-main/ecommerce/urls.py:1) : routes principales
- [accounts/views.py](/c:/Users/dell/Desktop/EMI/ecommerce_project-main/accounts/views.py:1) : logique d'inscription, confirmation email et profil
- [accounts/urls.py](/c:/Users/dell/Desktop/EMI/ecommerce_project-main/accounts/urls.py:1) : routes auth personnalisees
- [products/views.py](/c:/Users/dell/Desktop/EMI/ecommerce_project-main/products/views.py:1) : logique catalogue et panier
- [products/templates/layout.html](/c:/Users/dell/Desktop/EMI/ecommerce_project-main/products/templates/layout.html:1) : layout principal

## Tests manuels recommandes

1. Ouvrir `/products/`
2. Ouvrir `/products/1/`
3. Creer une inscription via `/accounts/signup/`
4. Verifier la reception du mail
5. Cliquer sur le lien de confirmation
6. Verifier la creation du compte et la connexion automatique
7. Acceder a `/accounts/profile/`
8. Modifier le profil
9. Changer le mot de passe
10. Tester la connexion avec le nouveau mot de passe

## Notes

- `db.sqlite3` est present dans le projet, mais la configuration active vise MySQL
- les medias sont stockes dans `images/`
- le fichier `.env` ne doit pas etre commit

## Git

Exemple de push :

```powershell
git add .
git commit -m "Update README and authentication flow"
git push
```
