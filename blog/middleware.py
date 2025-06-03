from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.urls import resolve
from blog.models import Article
import re
class AuthorPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        print(f"[Middleware] URL demandée : {path} par {request.user}")

        if re.match(r'^/fr/article/\d+/(modifier|supprimer)/$', path):
            if not request.user.is_authenticated:
                print("[Middleware] Utilisateur non authentifié")
                return HttpResponseForbidden("Authentification requise.")

            # Extraire l'ID de l'article de l'URL
            article_id = re.findall(r'\d+', path)[0]
            try:
                article = Article.objects.get(pk=article_id)
            except Article.DoesNotExist:
                return HttpResponseForbidden("Article introuvable.")

            # DEBUG
            print(f"article.auteur.pk = {article.auteur.pk}, request.user.pk = {request.user.pk}")
            print(f"Comparaison réussie ? {article.auteur.pk == request.user.pk}")

            # Vérification de l'auteur
            if article.auteur.pk != request.user.pk:
                print("[Middleware] Accès refusé : pas l'auteur.")
                return HttpResponseForbidden("Vous n'êtes pas l'auteur de cet article.")

        return self.get_response(request)
