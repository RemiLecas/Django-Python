from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Article

User = get_user_model()

class ArticleViewTests(TestCase):

    def setUp(self):
        # Création d'un utilisateur auteur et admin pour les tests
        self.user_author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='pass123'
        )
        self.user_author.is_author = True
        self.user_author.is_reader = True
        self.user_author.save()

        self.user_admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.user_admin.is_admin = True
        self.user_admin.is_reader = True
        self.user_admin.save()

        self.client = Client()

        # Article initial pour tests modif et suppression
        self.article = Article.objects.create(
            titre='Titre Test',
            contenu='Contenu test',
            auteur=self.user_author,
            slug='titre-test',
        )

    def test_ajouter_article_post_valide(self):
        self.client.login(username='author', password='pass123')
        url = reverse('ajouter_article')

        data = {
            'titre': 'Nouvel article',
            'contenu': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a,',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirection
        self.assertTrue(Article.objects.filter(titre='Nouvel article').exists())

    def test_modifier_article_post_valide(self):
        self.client.login(username='author', password='pass123')
        url = reverse('modifier_article', args=[self.article.id])

        data = {
            'titre': 'Titre modifié',
            'contenu': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a,',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.article.refresh_from_db()
        self.assertEqual(self.article.titre, 'Titre modifié')

    def test_supprimer_article_par_auteur(self):
        self.client.login(username='author', password='pass123')
        url = reverse('supprimer_article', args=[self.article.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())

    def test_supprimer_article_non_autorise(self):
        user = User.objects.create_user(username='user', password='pass123')
        self.client.login(username='user', password='pass123')

        url = reverse('supprimer_article', args=[self.article.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(id=self.article.id).exists())

    def test_supprimer_article_par_admin(self):
        self.client.login(username='admin', password='adminpass123')
        url = reverse('supprimer_article', args=[self.article.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())

