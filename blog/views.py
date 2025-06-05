from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Article, Categorie, Commentaire, Tag, CustomUser, Bookmark
from .forms import ArticleForm, CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
import logging
logger = logging.getLogger('app')
from functools import wraps
from django.db.models import Q, Count,Sum
from django.conf import settings
OPENAI_API_KEY = settings.OPENAI_API_KEY
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def role_required(min_role):
    roles_hierarchy = ['reader', 'author', 'editor', 'admin']

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentification requise.")

            user_role_index = roles_hierarchy.index(request.user.role) if request.user.role in roles_hierarchy else -1
            min_role_index = roles_hierarchy.index(min_role)

            if user_role_index >= min_role_index:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Accès refusé.")
        return _wrapped_view
    return decorator

def home(request):
    query = request.GET.get('q', '')
    categorie_id = request.GET.get('categorie')
    auteur_id = request.GET.get('auteur')
    tag_id = request.GET.get('tag')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    all_articles = Article.objects.filter(statut='published') \
        .select_related('auteur') \
        .prefetch_related('categories', 'tags')

    if auteur_id:
        auteur = CustomUser.objects.filter(id=auteur_id).first()
        if auteur:
            auteur_nom = auteur.get_full_name() or auteur.username
            all_articles = all_articles.filter(auteur=auteur)

    if categorie_id:
        categorie = Categorie.objects.filter(id=categorie_id).first()
        if categorie:
            categorie_nom = categorie.nom
            all_articles = all_articles.filter(categories=categorie)

    if tag_id:
        tag = Tag.objects.filter(id=tag_id).first()
        if tag:
            tag_nom = tag.nom
            all_articles = all_articles.filter(tags=tag)

    if date_min:
        all_articles = all_articles.filter(date_creation__gte=date_min)

    if date_max:
        all_articles = all_articles.filter(date_creation__lte=date_max)

    if query:
        all_articles = all_articles.filter(
            Q(titre__icontains=query) |
            Q(contenu__icontains=query) |
            Q(categories__nom__icontains=query) |
            Q(tags__nom__icontains=query) |
            Q(auteur__username__icontains=query) |
            Q(auteur__first_name__icontains=query) |
            Q(auteur__last_name__icontains=query)
        ).distinct()

    derniers_articles = all_articles.order_by('-date_creation')[:5]
    articles_populaires = all_articles.order_by('-vues')[:5]

    paginator = Paginator(all_articles.order_by('-date_creation'), 6)
    page_number = request.GET.get('page')
    page_articles = paginator.get_page(page_number)

    categories = Categorie.objects.all()
    auteurs = CustomUser.objects.filter(article__statut='published').distinct()
    tags = Tag.objects.annotate(article_count=Count('articles')).filter(article_count__gt=0).order_by('-article_count')[:20]

    categories_populaires = Categorie.objects.annotate(nb_articles=Count('articles')) \
                                 .filter(nb_articles__gt=0) \
                                 .order_by('-nb_articles')[:5]

    auteurs_populaires = CustomUser.objects.annotate(
        articles_publies_count=Count('article')
    ).order_by('-articles_publies_count')[:10]

    nb_articles = all_articles.count()

    return render(request, 'blog/home.html', {
        'derniers_articles': derniers_articles,
        'articles_populaires': articles_populaires,
        'articles': page_articles,
        'categories': categories,
        'auteurs': auteurs,
        'tags': tags,
        'categorie_id': categorie_id,
        'auteur_id': auteur_id,
        'tag_id': tag_id,
        'query': query,
        'date_min': date_min,
        'date_max': date_max,
        'categories_populaires': categories_populaires,
        'auteurs_populaires': auteurs_populaires,
        'nb_articles': nb_articles,

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
            logger.error(f"Erreur lors de l'ajout d'article par {request.user.username} : {form.errors}")
    else:
        form = ArticleForm()

    return render(request, 'blog/ajouter_article.html', {'form': form})

def details_article(request, slug):
    try:
        article = Article.objects.get(slug=slug)
        commentaires = article.commentaires.all()

    except Article.DoesNotExist:
            messages.error(request, "L'article demandé n'existe pas.")
            logger.warning(f"Article non trouvé pour le slug : {slug}")
            return redirect('home')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            logger.warning("Tentative de commenter sans être authentifié.")
            return redirect('login')
        contenu = request.POST.get('contenu')
        if contenu:
            Commentaire.objects.create(article=article, auteur=request.user, contenu=contenu)
            logger.info(f"Commentaire ajouté sur l'article '{article.titre}' par {request.user.username}")
            return redirect('details_article', slug=article.slug)


    article.vues += 1
    article.save(update_fields=['vues'])
    messages.info(request, f"Vous consultez l'article : {article.titre}")
    logger.info(f"Article '{article.titre}' consulté, vues = {article.vues}")

    return render(request, 'blog/details_article.html', {
        'article': article,
        'commentaires': commentaires,
    })

@login_required
def supprimer_article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        if article.auteur != request.user and request.user.role != 'admin':
            messages.error(request, "Vous n'êtes pas autorisé à supprimer cet article.")
            logger.warning(f"Utilisateur {request.user.username} a tenté de supprimer l'article ID {article_id} sans permission.")
            return redirect('home')

        article.delete()
        logger.info(f"Article ID {article_id} supprimé par {request.user.username}")
        messages.success(request, "Article supprimé avec succès.")
    except Article.DoesNotExist:
        logger.error(f"Tentative de suppression d'un article non-existant ID {article_id} par {request.user.username}")
        messages.error(request, "Article introuvable.")
    return redirect('home')

@login_required
@role_required('author')
def modifier_article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        logger.error(f"Tentative de modification d'un article non-existant ID {article_id} par {request.user.username}")
        messages.error(request, "Article introuvable.")
        return redirect('home')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            logger.info(f"Article ID {article_id} modifié par {request.user.username}")
            return redirect('details_article', slug=article.slug)
        else:
            logger.error(f"Erreur de modification article ID {article_id} par {request.user.username} : {form.errors}")
    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog/modifier_article.html', {'form': form, 'article': article})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f"Utilisateur connecté : {user.username}")
            return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
            logger.warning(f"Tentative de connexion échouée pour login : {request.POST.get('username')}")
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
    user = request.user

    articles = Article.objects.filter(auteur=user, statut='published') \
        .annotate(nb_likes=Count('likes', distinct=True), nb_comments=Count('commentaires', distinct=True))
    bookmarks = request.user.bookmarked_articles.all()

    nb_articles = articles.count()
    total_vues = articles.aggregate(total=Sum('vues'))['total'] or 0
    total_likes = articles.aggregate(total=Sum('nb_likes'))['total'] or 0
    total_comments = articles.aggregate(total=Sum('nb_comments'))['total'] or 0

    brouillons = Article.objects.filter(auteur=user, statut='draft')
    my_articles = Article.objects.filter(auteur=request.user, statut='published').order_by('-date_creation')
    context = {
        'user': user,
        'nb_articles': nb_articles,
        'total_vues': total_vues,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'bookmarks': bookmarks,
        'brouillons': brouillons,
        'my_articles': my_articles
    }

    return render(request, 'blog/dashboard.html', context)
@login_required()
def publier_article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        article.statut = 'published'
        article.save()
        messages.success(request, f"L'article '{article.titre}' a été publié.")
        logger.info(f"Article ID {article_id} publié par {request.user.username}")
    except Article.DoesNotExist:
        messages.error(request, "Article introuvable.")
        logger.error(f"Tentative de publication d'article non-existant ID {article_id} par {request.user.username}")
    return redirect('dashboard')

@login_required()
def supprimer_commentaire(request, commentaire_id):
    try:
        commentaire = Commentaire.objects.get(id=commentaire_id)
        article = commentaire.article
    except Commentaire.DoesNotExist:
        logger.error(f"Tentative suppression commentaire inexistant ID {commentaire_id} par {request.user.username}")
        messages.error(request, "Commentaire introuvable.")
        return redirect('home')

    if request.user != article.auteur and not request.user.is_admin:
        logger.warning(f"Utilisateur {request.user.username} non autorisé à supprimer commentaire ID {commentaire_id}")
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce commentaire.")

    if request.method == "POST":
        commentaire.delete()
        logger.info(f"Commentaire ID {commentaire_id} supprimé par {request.user.username}")
        return redirect(article.get_absolute_url())

    return redirect(article.get_absolute_url())

@receiver(post_save, sender=Article)
@receiver(post_delete, sender=Article)
def update_article_count_on_save_or_delete(sender, instance, **kwargs):
    Categorie.update_article_counts()

@receiver(m2m_changed, sender=Article.categories.through)
def update_article_count_on_m2m_change(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        Categorie.update_article_counts()

@login_required
def like_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.toggle_like(request.user)
    return redirect(request.META.get('HTTP_REFERER', reverse('details_article', kwargs={'slug': slug})))


@login_required
def bookmark_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.toggle_bookmark(request.user)
    return redirect(request.META.get('HTTP_REFERER', reverse('details_article', kwargs={'slug': slug})))

    return redirect('details_article', slug=slug)

@login_required
@require_POST
def toggle_bookmark(request, slug):
    article = get_object_or_404(Article, slug=slug)
    user = request.user
    if article in user.bookmarks.all():
        user.bookmarks.remove(article)
    else:
        user.bookmarks.add(article)
    return redirect(article.get_absolute_url())

def articles_view(request):
    categorie_id = request.GET.get('categorie')

    categories = Categorie.objects.annotate(
        published_count=Count('articles', filter=Q(articles__statut='published'))
    ).order_by('-published_count', 'nom')

    articles = Article.objects.filter(statut='published')
    if categorie_id:
        articles = articles.filter(categories__id=categorie_id)

    articles = articles.order_by('-date_creation')

    # Pagination
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_articles = paginator.get_page(page_number)

    return render(request, 'blog/articles.html', {
        'categories': categories,
        'articles': page_articles,
    })

@login_required
def generer_article_chatgpt(request):
    if request.method == "POST":
        data = json.loads(request.body)
        titre = data.get("titre", "")
        if not titre:
            return JsonResponse({"error": "Titre manquant."}, status=400)

        contenu, image_url = generer_contenu_et_image(titre)
        return JsonResponse({
            "contenu": contenu,
            "image_url": image_url
        })
    return JsonResponse({"error": "Méthode non autorisée."}, status=405)

def generer_contenu_et_image(titre):
    # Générer contenu via ChatGPT
    prompt = f"Rédige un article sur : {titre}"
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
        }
    )
    contenu = ""
    if response.status_code == 200:
        contenu = response.json()["choices"][0]["message"]["content"]
    else:
        contenu = "Erreur lors de la génération du contenu."

    # Générer image via DALL·E
    image_prompt = f"Illustration pour : {titre}"
    img_response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
        json={"prompt": image_prompt, "n": 1, "size": "512x512"}
    )
    image_url = ""
    if img_response.status_code == 200:
        image_url = img_response.json()["data"][0]["url"]
    else:
        image_url = ""

    return contenu, image_url
class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/custom_password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    success_message = "Un e-mail de réinitialisation vous a été envoyé si cette adresse est enregistrée."

