from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MinValueValidator

from Members.models import Profile, Message, CustomUser
from fields import FIELD_CHOICES
from storages.backends.s3boto3 import S3Boto3Storage


'''choices = Category.objects.all().values_list('category', 'category')
choice_list = []
for item in choices:
    choice_list.append(item)'''

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class CreateProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture', 'first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

class EditProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'profile_picture']  # Include 'profile_picture' in the fields
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Adjust fields based on user's verification status
        if user and user.is_expert:
            self.fields['github_url'] = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
            self.fields['linkedin_url'] = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

            self.fields['university'] = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
            self.fields['job_history'] = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
            # Update Meta fields to include all fields for verified users
            self.Meta.fields += ['github_url', 'linkedin_url', 'academic_field', 'university', 'job_history']
            # Include any additional fields for verified users
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