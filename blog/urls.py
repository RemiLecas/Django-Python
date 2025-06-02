from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('ajouter/', views.ajouter_article, name='ajouter_article'),
    path('details/<int:id>/', views.details_article, name='details_article'),
    path('article/<int:article_id>/supprimer/', views.supprimer_article, name='supprimer_article'),
    path('article/<int:article_id>/modifier/', views.modifier_article, name='modifier_article'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
