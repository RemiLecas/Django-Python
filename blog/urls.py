from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    path('', views.home, name='home'),
    path('ajouter/', views.ajouter_article, name='ajouter_article'),
    path('details/<int:id>/', views.details_article, name='details_article'),
    path('article/<int:article_id>/supprimer/', views.supprimer_article, name='supprimer_article'),
    path('article/<int:article_id>/modifier/', views.modifier_article, name='modifier_article'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/publier/<int:article_id>/', views.publier_article, name='publier_article'),
    path('commentaire/<int:commentaire_id>/supprimer/', views.supprimer_commentaire, name='supprimer_commentaire'),
    path("mot-de-passe-oublie/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("mot-de-passe-envoye/", auth_views.PasswordResetDoneView.as_view(template_name='registration/custom_password_reset_done.html'), name="password_reset_done"),
    path("reinitialiser/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='registration/custom_password_reset_confirm.html'), name="password_reset_confirm"),
    path("reinitialisation-terminee/", auth_views.PasswordResetCompleteView.as_view(template_name='registration/custom_password_reset_complete.html'), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

