from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'auteur', 'commentaire', 'categories', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': "Titre de l'article"}),
            'contenu': forms.Textarea(attrs={'rows':5, 'placeholder': 'Contenu'}),
            'auteur': forms.TextInput(attrs={'placeholder': "Nom de l'auteur"}),
            'commentaire': forms.TextInput(attrs={'placeholder': 'Commentaire'}),
            'categories': forms.SelectMultiple(attrs={'size': 5}),
        }
