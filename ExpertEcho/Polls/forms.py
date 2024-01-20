from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import formset_factory
from .models import Poll, Choice
from Blogs.models import Category

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'category']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice']

ChoiceFormSet = formset_factory(ChoiceForm, extra=1, min_num=1, validate_min=True)