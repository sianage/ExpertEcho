from django.forms import TextInput, CharField

from Blogs.models import Post, CustomUser
from Debates.models import Comment
from Homepage.models import Note
from .models import Debate
from django import forms
from Members.models import Profile, Message

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class DebateForm(forms.ModelForm):
    def __init__(self, *args, opponent_choices=None, **kwargs):
        super().__init__(*args, **kwargs)

        if opponent_choices:
            self.fields['opponent'].choices = opponent_choices


    class Meta:
        model = Debate
        fields = ('opponent', 'description', 'title')

        widgets = {
            'opponent': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def set_opponent_choices(self, opponent_choices):
        self.fields['opponent'].choices = opponent_choices

