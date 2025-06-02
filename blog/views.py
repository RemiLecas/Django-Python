from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Article, Categorie
from .forms import ArticleForm
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def home(request):
    message = _("Hello, world!")
    print(message)
    categorie_id = request.GET.get('categorie')  # Récupère la catégorie choisie dans l'URL
    categories = Categorie.objects.all()  # Toutes les catégories pour le select

    if categorie_id:
        articles = Article.objects.filter(categories__id=categorie_id).distinct()
    else:
        articles = Article.objects.all()

    return render(request, 'blog/home.html', {
        'articles': articles,
        'categories': categories,
        'categorie_id': categorie_id
    })

def ajouter_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article ajouté avec succès!')
            return redirect('home')
    else:
        form = ArticleForm()

    return render(request, 'blog/ajouter_article.html', {'form': form})

def details_article(request, id):
    try:
        article = Article.objects.get(pk=id)
    except Article.DoesNotExist:
        messages.error(request, "L'article demandé n'existe pas.")
        return redirect('home')

    messages.info(request, f"Vous consultez l'article : {article.titre}")
    return render(request, 'blog/details_article.html', {'article': article})

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
