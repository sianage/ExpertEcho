from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author_profile', 'body', 'status')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author_profile': forms.HiddenInput(),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }