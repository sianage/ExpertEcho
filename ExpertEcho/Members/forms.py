from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from Members.models import Profile, Message, CustomUser
from fields import FIELD_CHOICES
from storages.backends.s3boto3 import S3Boto3Storage


'''choices = Category.objects.all().values_list('category', 'category')
choice_list = []
for item in choices:
    choice_list.append(item)'''

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class CreateProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    github_url = forms.CharField(max_length=255)
    linkedin_url = forms.CharField(max_length=255)
    academic_field = forms.ChoiceField(choices=FIELD_CHOICES)

    class Meta:
        model = Profile
        fields = ('bio', 'github_url', 'linkedin_url', 'academic_field', 'profile_picture', 'first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'github_url': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_field': forms.Select(choices=FIELD_CHOICES, attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

class EditProfileForm(UserChangeForm):
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    github_url = forms.CharField(max_length=255)
    linkedin_url = forms.CharField(max_length=255)
    academic_field = forms.ChoiceField(choices=FIELD_CHOICES)

    class Meta:
        model = Profile
        fields = ('bio', 'github_url', 'linkedin_url', 'academic_field', 'profile_picture', 'first_name', 'last_name')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'github_url': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_field': forms.Select(choices=FIELD_CHOICES, attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class EditSettingsForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class EditPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']