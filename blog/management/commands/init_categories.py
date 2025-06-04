from django.core.management.base import BaseCommand
from blog.models import Categorie
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Crée des catégories par défaut'

    def handle(self, *args, **kwargs):
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
