import sys

from ckeditor.fields import RichTextField

#print(sys.path)

sys.path.append('C:/Users/siana/OneDrive/Desktop/ExpertEcho/ExpertEcho')

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from fields import FIELD_CHOICES
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        #converts to lowercase
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        #hashes password
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    #checks if entered password matches stored hashed password
    def check_password(self, user, password):
        return check_password(password, user.password)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_expert = models.BooleanField(default=False)  # Identifies if the user is an expert
    date_joined = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(Group, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followed_by', blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    # Expert-specific fields
    years_of_experience = models.IntegerField(
        validators=[MinValueValidator(5)], default=5,
        help_text="Enter your years of experience (minimum: 5)"
    )
    has_masters = models.BooleanField(default=False)
    has_phd = models.BooleanField(default=False)
    university = models.CharField(max_length=100)
    job_history = models.TextField(blank=True)
    academic_field = models.CharField(max_length=20, choices=FIELD_CHOICES, default='None Selected')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    # Additional fields based on user type
    is_public_profile = models.BooleanField(default=False)
    can_create_content = models.BooleanField(default=False)

    def __str__(self):
        return f'Profile for {self.user.email}'

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['timestamp']

class Note(models.Model):
    user = models.ForeignKey(CustomUser, related_name="user_notes", on_delete=models.DO_NOTHING)
    body = RichTextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    author_profile = models.ForeignKey(Profile, related_name="profile_notes", on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return (
            f"{self.user} \n"
            f" {self.body}\n"
            f"(Note made {self.created:%Y-%m-%d %H:%M})"
        )