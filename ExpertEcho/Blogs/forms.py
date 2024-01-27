from django.forms import TextInput, CharField

from .models import Post, Category
from django import forms
# hard-coded version of selection list of categories (not used)
#choices = [('economics', 'economics'), ('philosophy', 'philosophy'), ('medicine', 'medicine'), ('politics', 'politics')]
choices = Category.objects.all().values_list('category', 'category')
choice_list = []
for item in choices:
    choice_list.append(item)

authors = Post.objects.all().values_list('author', 'author')
author_list = []
for person in authors:
    author_list.append(person)

class PostForm(forms.ModelForm):
    '''def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = user.profile.field'''
    class Meta:
        model = Post
        fields = ('title', 'author', 'body', 'header_image', 'status')
        #exclude = ('author', 'slug', 'publish', 'category')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'username', 'id':'user', 'type':'hidden'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }