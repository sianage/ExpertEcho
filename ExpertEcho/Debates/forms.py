from django.forms import TextInput, CharField

from Blogs.models import Post, Category, CustomUser
from Debates.models import Comment
from Homepage.models import Note
from .models import Debate
from django import forms
from Members.models import Profile, Message
from Blogs.forms import author_list, choice_list

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commenter_name','body')

        widgets = {
            'commenter_name':forms.Select(choices=author_list, attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class DebateForm(forms.ModelForm):
    class Meta:
        model = Debate
        fields = ('category', 'author', 'opponent', 'description', 'title')

        widgets = {
            'category':forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'author':forms.Select(choices=author_list, attrs={'class': 'form-control'}),
            'opponent':forms.Select(choices=author_list, attrs={'class': 'form-control'}),
            'title':forms.TextInput(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control'}),
        }