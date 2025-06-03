from django.core.management.base import BaseCommand
from blog.models import Categorie
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Crée des catégories par défaut'

    def handle(self, *args, **kwargs):
        categories = [
            {'nom': 'Technologie', 'description': 'Articles sur la technologie', 'icone': 'fa-tech'},
            {'nom': 'Sport', 'description': 'Articles sur le sport', 'icone': 'fa-football-ball'},
            {'nom': 'Cuisine', 'description': 'Articles sur la cuisine', 'icone': 'fa-utensils'},
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
