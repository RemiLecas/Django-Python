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

        if re.match(r'^/fr/article/\d+/(modifier|supprimer)/$', path):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentification requise.")

            article_id = int(re.findall(r'\d+', path)[0])
            article = get_object_or_404(Article, pk=article_id)

            if request.user.role == 'author' and article.auteur != request.user:
                return HttpResponseForbidden("Vous n'êtes pas l'auteur de cet article.")

            # éditeurs et admins ont accès
        return self.get_response(request)

