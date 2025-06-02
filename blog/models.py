from django.db import models
from django.utils import timezone

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.CharField(max_length=100)
    date_creation = models.DateTimeField(default=timezone.now)
    commentaire = models.CharField(max_length=100, default='')
    categories = models.ManyToManyField(Categorie, related_name='articles')
    image = models.ImageField(upload_to='articles_images/', null=True, blank=True)

def __str__(self):
    return self.titre

    class Meta:
        ordering = ['-date_creation']
