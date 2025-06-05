from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Tag, Categorie
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Crée des catégories, tags et utilisateurs par défaut'

    def handle(self, *args, **kwargs):
        # Création des catégories
        categories = [
            {'nom': 'Technologie', 'description': 'Articles sur la technologie', 'icone': 'fa-microchip'},
            {'nom': 'Sport', 'description': 'Articles sur le sport', 'icone': 'fa-football-ball'},
            {'nom': 'Cuisine', 'description': 'Articles sur la cuisine', 'icone': 'fa-utensils'},
            {'nom': 'Voyage', 'description': 'Conseils et récits de voyage', 'icone': 'fa-plane'},
            {'nom': 'Santé', 'description': 'Bien-être, nutrition et médecine', 'icone': 'fa-heartbeat'},
            {'nom': 'Éducation', 'description': 'Apprentissage, études et pédagogie', 'icone': 'fa-graduation-cap'},
            {'nom': 'Divertissement', 'description': 'Films, séries, jeux et loisirs', 'icone': 'fa-film'},
            {'nom': 'Business', 'description': 'Actualités économiques et conseils professionnels', 'icone': 'fa-briefcase'},
            {'nom': 'Mode', 'description': 'Tendances vestimentaires et conseils style', 'icone': 'fa-tshirt'},
            {'nom': 'Art & Culture', 'description': 'Peinture, musique, littérature et plus', 'icone': 'fa-palette'},
            {'nom': 'Science', 'description': 'Découvertes et avancées scientifiques', 'icone': 'fa-atom'},
            {'nom': 'Environnement', 'description': 'Écologie, développement durable', 'icone': 'fa-leaf'},
            {'nom': 'Finance', 'description': 'Épargne, investissement, cryptomonnaies', 'icone': 'fa-coins'},
        ]

        for cat in categories:
            slug = slugify(cat['nom'])
            obj, created = Categorie.objects.get_or_create(slug=slug, defaults={
                'nom': cat['nom'],
                'description': cat['description'],
                'icone': cat['icone'],
            })
            if created:
                self.stdout.write(self.style.SUCCESS(f"Catégorie '{cat['nom']}' créée"))
            else:
                self.stdout.write(f"Catégorie '{cat['nom']}' déjà existante")

        # Création des tags
        tags = [
            'Python',
            'Django',
            'React',
            'Machine Learning',
            'Fitness',
            'Nutrition',
            'Voyage',
            'Photographie',
            'Musique',
            'Finances',
            'Crypto',
            'Design',
            'Jeux Vidéo',
            'Écologie',
            'Startup',
            'Lecture',
            'Cinéma',
        ]

        for tag_name in tags:
            slug = slugify(tag_name)
            obj, created = Tag.objects.get_or_create(slug=slug, defaults={
                'nom': tag_name,
            })
            if created:
                self.stdout.write(self.style.SUCCESS(f"Tag '{tag_name}' créé"))
            else:
                self.stdout.write(f"Tag '{tag_name}' déjà existant")

        users = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "password": "admin123",
                "is_reader": True,
                "is_author": True,
                "is_editor": True,
                "is_admin": True,
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "username": "auteur1",
                "email": "auteur1@example.com",
                "password": "pass123",
                "is_reader": True,
                "is_author": True,
                "is_editor": False,
                "is_admin": False,
                "is_staff": False,
                "is_superuser": False,
            },
            {
                "username": "auteur2",
                "email": "auteur2@example.com",
                "password": "pass123",
                "is_reader": True,
                "is_author": True,
                "is_editor": False,
                "is_admin": False,
                "is_staff": False,
                "is_superuser": False,
            },
            {
                "username": "lecteur1",
                "email": "lecteur1@example.com",
                "password": "pass123",
                "is_reader": True,
                "is_author": False,
                "is_editor": False,
                "is_admin": False,
                "is_staff": False,
                "is_superuser": False,
            },
            {
                "username": "lecteur2",
                "email": "lecteur2@example.com",
                "password": "pass123",
                "is_reader": True,
                "is_author": False,
                "is_editor": False,
                "is_admin": False,
                "is_staff": False,
                "is_superuser": False,
            },
            {
                "username": "editor1",
                "email": "editor1@example.com",
                "password": "pass123",
                "is_reader": True,
                "is_author": False,
                "is_editor": True,
                "is_admin": False,
                "is_staff": False,
                "is_superuser": False,
            },
            {
                "username": "editor2",
                "email": "editor2@example.com",
                "password": "pass123",
                "is_reader": True,
                "is_author": False,
                "is_editor": True,
                "is_admin": False,
                "is_staff": False,
                "is_superuser": False,
            },
        ]

        for u in users:
            user, created = CustomUser.objects.get_or_create(
                username=u["username"],
                defaults={
                    "email": u["email"],
                    "is_reader": u["is_reader"],
                    "is_author": u["is_author"],
                    "is_editor": u["is_editor"],
                    "is_admin": u["is_admin"],
                    "is_staff": u["is_staff"],
                    "is_superuser": u["is_superuser"],
                }
            )
            if created:
                user.set_password(u["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Utilisateur '{u['username']}' créé"))
            else:
                self.stdout.write(f"Utilisateur '{u['username']}' déjà existant")
