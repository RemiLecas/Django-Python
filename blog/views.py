from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from .models import Article, Categorie, Commentaire
from .forms import ArticleForm, CustomUserCreationForm
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

import logging
logger = logging.getLogger(__name__)
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Accès refusé.")
        return _wrapped_view
    return decorator

def home(request):
    categorie_id = request.GET.get('categorie')
    query = request.GET.get('q', '')
    categories = Categorie.objects.all()
    articles = Article.objects.all()

    if categorie_id:
        articles = articles.filter(categories__id=categorie_id)

    if query:
        articles = articles.filter(
            Q(titre__icontains=query) |
            Q(contenu__icontains=query) |
            Q(categories__nom__icontains=query)
        ).distinct()

    return render(request, 'blog/home.html', {
        'articles': articles,
        'categories': categories,
        'categorie_id': categorie_id,
        'query': query
    })

@login_required
def ajouter_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.save()
            form.save_m2m()
            messages.success(request, 'Article ajouté avec succès !')
            return redirect('home')
        else:
            logger.error(form.errors)
    else:
        form = ArticleForm()

    return render(request, 'blog/ajouter_article.html', {'form': form})

def details_article(request, id):
    try:
        article = Article.objects.get(pk=id)
        commentaires = article.commentaires.all()

    except Article.DoesNotExist:
            messages.error(request, "L'article demandé n'existe pas.")
            return redirect('home')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        contenu = request.POST.get('contenu')
        if contenu:
            Commentaire.objects.create(article=article, auteur=request.user, contenu=contenu)
            return redirect('details_article', id=article.id)

    article.vues += 1
    article.save(update_fields=['vues'])
    messages.info(request, f"Vous consultez l'article : {article.titre}")

    return render(request, 'blog/details_article.html', {
        'article': article,
        'commentaires': commentaires,
    })
def supprimer_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.delete()
    return redirect('home')

def modifier_article(request, article_id):
    article = Article.objects.get(pk=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('details_article', id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog/modifier_article.html', {'form': form, 'article': article})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
            # Ici, si le formulaire est invalide, tu n'as pas défini `form` dans ce bloc else
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    brouillons = Article.objects.filter(auteur=request.user, statut='draft').order_by('-date_creation')

    return render(request, 'blog/dashboard.html', {
        'user': request.user,
        'brouillons': brouillons
    })

@login_required()
def publier_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.statut = 'published'
    article.save()
    messages.success(request, f"L'article '{article.titre}' a été publié.")
    return redirect('dashboard')

@login_required()
def supprimer_commentaire(request, commentaire_id):
    commentaire = Commentaire.objects.get(id=commentaire_id)
    article = commentaire.article

    if request.user != article.auteur and not request.user.is_admin:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce commentaire.")

    if request.method == "POST":
        commentaire.delete()
        return redirect(article.get_absolute_url())

    return redirect(article.get_absolute_url())

class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/custom_password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    success_message = "Un e-mail de réinitialisation vous a été envoyé si cette adresse est enregistrée."
