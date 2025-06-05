from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Count, Q
import math
import re
from django.core.exceptions import ValidationError

def validate_contenu(value):
    if len(value) < 100:
        raise ValidationError("Le contenu doit faire au moins 100 caractères.")

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_reader = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    bookmarks = models.ManyToManyField('Article', related_name='bookmarked_by', blank=True)

    @property
    def role(self):
        if self.is_admin:
            return 'admin'
        elif self.is_editor:
            return 'editor'
        elif self.is_author:
            return 'author'
        elif self.is_reader:
            return 'reader'
        return 'reader'

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    icone = models.CharField(max_length=50, blank=True)
    article_count = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['nom']
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_category_slug')
        ]

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


    @classmethod
    def update_article_counts(cls):
        categories = cls.objects.annotate(
            count=Count('articles', filter=Q(articles__statut='published'))
        )
        for category in categories:
            cls.objects.filter(id=category.id).update(article_count=category.count)

class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})

    @classmethod
    def get_popular_tags(cls, limit=10):
        return cls.objects.annotate(num_articles=Count('articles')).order_by('-num_articles')[:limit]

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
    contenu = models.TextField(validators=[validate_contenu])
    extrait = models.TextField(blank=True)
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Categorie, related_name='articles', blank=True)
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='draft')
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    vues = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(CustomUser, related_name='liked_articles', blank=True)
    bookmarks = models.ManyToManyField(CustomUser, related_name='bookmarked_articles', blank=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('details_article', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        if not self.extrait:
            self.extrait = self.contenu[:150] + '...' if len(self.contenu) > 150 else self.contenu
        super().save(*args, **kwargs)

    def temps_lecture(self):
        words = len(re.findall(r'\w+', self.contenu))
        minutes = max(1, math.ceil(words / 200))
        return minutes

    def total_likes(self):
        return self.likes.count()

    def toggle_like(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
            return False
        else:
            self.likes.add(user)
            return True

    def toggle_bookmark(self, user):
        if user in self.bookmarks.all():
            self.bookmarks.remove(user)
            return False
        else:
            self.bookmarks.add(user)
            return True

    def total_bookmarks(self):
        return self.bookmarks.count()

class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f'Commentaire de {self.auteur} sur {self.article}'


class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')
