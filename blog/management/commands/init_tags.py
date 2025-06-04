from django.core.management.base import BaseCommand
from blog.models import Tag
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Crée des tags par défaut'

    def handle(self, *args, **kwargs):
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
