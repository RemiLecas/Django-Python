Installation et configuration
1. Créer un environnement virtuel Python
``bash python -m venv venv
   .\venv\Scripts\Activate.ps1
   ``
Une fois activé, installez les dépendances du projet :

bash
pip install -r requirements.txt

Pour désactiver l’environnement virtuel, tapez simplement :

``bash deactivate``

2. Initialiser la base de données avec des données par défaut
   Pour peupler la base avec les catégories, tags et utilisateurs par défaut, exécutez la commande personnalisée Django dans le projet :
``bash python manage.py init_data
   ``

Cette commande va :
-   Créer les catégories par défaut (Technologie, Sport, Cuisine, etc.),
-   Créer les tags courants (Python, Django, React, ...),
-   Créer les utilisateurs avec différents rôles.

3. Utilisateurs et rôles dans l’application
   L’application gère différents types d’utilisateurs, chacun avec des permissions spécifiques :
| Rôle        | Description                                      | Ce qu’il peut faire                                                                            |
   | ----------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
   | **Admin**   | Super-utilisateur avec tous les droits           | Gestion complète de l’application, création et modération de contenu, gestion des utilisateurs |
   | **Auteur**  | Utilisateur qui peut créer et gérer ses articles | Créer, modifier, supprimer ses articles                                                        |
   | **Lecteur** | Utilisateur standard                             | Lire les articles, commenter                                                                   |
   | **Éditeur** | Peut modérer et valider le contenu               | modifier des articles créés par les auteurs                              |

4. Connexion et utilisation
Utilisez les comptes créés lors de l'initialisation pour vous connecter à l’application.
Un compte admin est disponible avec :
Username : admin
Password : admin123

Les auteurs (auteur1, auteur2) peuvent gérer leur contenu.
Les lecteurs (lecteur1, lecteur2) ont accès en lecture seule.
Les editeurs (editeur1, editeur2) peuvent modifier des articles.

