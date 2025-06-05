# Installation et configuration
## 1. Créer un environnement virtuel Python
````bash python -m venv django_env````
puis
````bash .\django_env\Scripts\Activate ````

Une fois activé, installez les dépendances du projet :
```bash pip install -r requirements.txt```

Ensuite vous pouvez vous créez différent environnement avec les commandes suivantes
Pour être en dev:
```bash $env:DJANGO_ENV="dev"```
Pour être en prod:
```bash $env:DJANGO_ENV="prod"```

pour voir l'environnement selectionner il faut faire 
```bash echo $env:DJANGO_ENV```

Pour désactiver l’environnement virtuel, tapez simplement :

```bash deactivate```

## 2. Configuration du fichier .env et views
Avant d'initialiser la base de données, il est indispensable de configurer le fichier .env à la racine du projet.
```
DJANGO_SECRET_KEY=

DEV_DB_NAME=
DEV_DB_USER=
DEV_DB_PASSWORD=
DEV_DB_HOST=
DEV_DB_PORT=

PROD_DB_NAME=
PROD_DB_USER=
PROD_DB_PASSWORD=
PROD_DB_HOST=
PROD_DB_PORT=

# Avec Mail Trap
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=2525

```

et dans le views.py il faut mettre votre clé OPENAI_API_KEY 
```OPENAI_API_KEY=votre_clef_api_openai_ici```

## 3. Initialiser la base de données avec des données par défaut
Quand vous avez créer votre base de données et rentré les informations nécessaire dans le .env il faudra exécuté ces 2 commandes
```bash python manage.py makemigrations```
puis
```bash python manage.py migrate```

Cela aura pour conséquence d'instancié les tables de la base.

Une fois cela fais on peut peupler notre base de données.
Pour peupler la base avec les catégories, tags et utilisateurs par défaut, exécutez la commande personnalisée Django dans le projet :
```bash python manage.py init_data```

Cette commande va :
-   Créer les catégories par défaut (Technologie, Sport, Cuisine, etc.),
-   Créer les tags courants (Python, Django, React, ...),
-   Créer les utilisateurs avec différents rôles.

## 4. Utilisateurs et rôles dans l’application
   L’application gère différents types d’utilisateurs, chacun avec des permissions spécifiques :
| Rôle        | Description                                      | Ce qu’il peut faire                                                                            |
   | ----------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
   | **Admin**   | Super-utilisateur avec tous les droits           | Gestion complète de l’application, création et modération de contenu, gestion des utilisateurs |
   | **Auteur**  | Utilisateur qui peut créer et gérer ses articles | Créer, modifier, supprimer ses articles                                                        |
   | **Lecteur** | Utilisateur standard                             | Lire les articles, commenter                                                                   |
   | **Éditeur** | Peut modérer et valider le contenu               | modifier des articles créés par les auteurs                              |

## 5. Routes disponibles
| URL                                            | Nom de la route           | Description                      |
| ---------------------------------------------- | ------------------------- | -------------------------------- |
| `/`                                            | `home`                    | Page d’accueil                   |
| `/ajouter/`                                    | `ajouter_article`         | Ajouter un nouvel article        |
| `/article/<slug:slug>/`                        | `details_article`         | Détails d’un article             |
| `/article/<int:article_id>/supprimer/`         | `supprimer_article`       | Supprimer un article             |
| `/article/<int:article_id>/modifier/`          | `modifier_article`        | Modifier un article              |
| `/login/`                                      | `login`                   | Page de connexion                |
| `/register/`                                   | `register`                | Page d’inscription               |
| `/logout/`                                     | `logout`                  | Déconnexion                      |
| `/dashboard/`                                  | `dashboard`               | Tableau de bord utilisateur      |
| `/dashboard/publier/<int:article_id>/`         | `publier_article`         | Publier un article               |
| `/commentaire/<int:commentaire_id>/supprimer/` | `supprimer_commentaire`   | Supprimer un commentaire         |
| `/mot-de-passe-oublie/`                        | `password_reset`          | Mot de passe oublié              |
| `/mot-de-passe-envoye/`                        | `password_reset_done`     | Confirmation d’envoi email reset |
| `/reinitialiser/<uidb64>/<token>/`             | `password_reset_confirm`  | Réinitialisation du mot de passe |
| `/reinitialisation-terminee/`                  | `password_reset_complete` | Fin de la réinitialisation       |
| `/article/<slug:slug>/like/`                   | `like_article`            | Liker/unliker un article         |
| `/article/<slug:slug>/bookmark/`               | `bookmark_article`        | Ajouter/supprimer un favori      |
| `/bookmark/toggle/<slug:slug>/`                | `toggle_bookmark`         | Basculer le favori               |
| `/articles/`                                   | `articles`                | Liste des articles               |
| `/generer-article-chatgpt/`                    | `generer_article_chatgpt` | Générer un article via ChatGPT   |


## 6. Lancement du projet
Pour lancer le projet il suffit simplement de taper la commande ```bash python manage.py runserver```

## 7. Connexion et utilisation
Utilisez les comptes créés lors de l'initialisation pour vous connecter à l’application.
| Username | Rôle    | Mot de passe |
| -------- | ------- | ------------ |
| admin    | Admin   | admin123     |
| auteur1  | Auteur  | password123  |
| lecteur1 | Lecteur | password123  |
| editeur1 | Éditeur | password123  |

## 8. Lancer les tests
Pour exécuter les tests automatisés, lancez la commande :
```bash python manage.py test```
