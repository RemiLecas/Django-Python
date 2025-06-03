from django import forms
from .models import Article, CustomUser
from django.contrib.auth.forms import UserCreationForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'commentaire', 'categories', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': "Titre de l'article"}),
            'contenu': forms.Textarea(attrs={'rows':5, 'placeholder': 'Contenu'}),
            'commentaire': forms.TextInput(attrs={'placeholder': 'Commentaire'}),
            'categories': forms.SelectMultiple(attrs={'size': 5}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_reader = True
        user.is_author = False
        user.is_editor = False
        user.is_admin = False
        if commit:
            user.save()
        return user
