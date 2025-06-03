from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Count

class CustomUser(AbstractUser):
    is_reader = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    icone = models.CharField(max_length=50, blank=True)  # Par ex. nom d'icône fontawesome

    class Meta:
        ordering = ['nom']
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_category_slug')
        ]

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    @property
    def article_count(self):
        # Compte dynamique des articles liés à cette catégorie
        return self.article_set.count()

    def save(self, *args, **kwargs):
        # Génère le slug automatiquement si absent
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})

    @classmethod
    def get_popular_tags(cls, limit=10):
        # Retourne les tags les plus utilisés par nombre d'articles
        return cls.objects.annotate(num_articles=Count('article')).order_by('-num_articles')[:limit]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

class Article(models.Model):
    STATUT_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('archived', 'Archivé'),
    ]

    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    contenu = models.TextField()
    extrait = models.TextField(blank=True)
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Categorie, related_name='articles', blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='draft')
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    vues = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('details_article', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        # Génère automatiquement un slug à partir du titre si vide
        if not self.slug:
            self.slug = slugify(self.titre)
        # Génère un extrait si vide (ex: 150 premiers caractères)
        if not self.extrait:
            self.extrait = self.contenu[:150] + '...' if len(self.contenu) > 150 else self.contenu
        super().save(*args, **kwargs)


class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f'Commentaire de {self.auteur} sur {self.article}'
