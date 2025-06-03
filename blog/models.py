from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    is_reader = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    commentaire = models.CharField(max_length=100, blank=True, default='')
    categories = models.ManyToManyField(Categorie, related_name='articles')
    image = models.ImageField(upload_to='articles_images/', null=True, blank=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

        class Meta:
            ordering = ['-date_creation']
