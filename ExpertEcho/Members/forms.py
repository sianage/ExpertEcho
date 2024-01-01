from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from MainApp.models import Profile
from storages.backends.s3boto3 import S3Boto3Storage


from MainApp.models import Profile, Category
choices = Category.objects.all().values_list('category', 'category')
choice_list = []
for item in choices:
    choice_list.append(item)


class ProfilePageForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    github_url = forms.CharField(max_length=255)
    linkedin_url = forms.CharField(max_length=255)
    academic_field = forms.ChoiceField(choices=choice_list)

    class Meta:
        model = Profile
        fields = ('bio', 'github_url', 'linkedin_url', 'academic_field', 'profile_picture')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'github_url': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_field': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class EditProfileForm(UserChangeForm):
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    github_url = forms.CharField(max_length=255)
    linkedin_url = forms.CharField(max_length=255)
    academic_field = forms.ChoiceField(choices=choice_list)

    class Meta:
        model = Profile
        fields = ('bio', 'github_url', 'linkedin_url', 'academic_field', 'profile_picture')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'github_url': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_field': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class EditSettingsForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class EditPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']