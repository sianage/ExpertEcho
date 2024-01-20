import sys
#print(sys.path)

sys.path.append('C:/Users/siana/OneDrive/Desktop/ExpertEcho/ExpertEcho')  # Replace with the actual path to ExpertEcho

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from fields import FIELD_CHOICES
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator

class AcademicField(models.Model):
    name = models.CharField(max_length=30, choices=FIELD_CHOICES, unique=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def check_password(self, user, password):
        return check_password(password, user.password)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_expert = models.BooleanField(default=False)  # Identifies if the user is an expert
    date_joined = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(Group, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    follows = models.ManyToManyField(CustomUser, related_name='followed_by', blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    # Expert-specific fields
    years_of_experience = models.IntegerField(
        validators=[MinValueValidator(5)],
        help_text="Enter your years of experience (minimum: 5)"
    )
    has_masters = models.BooleanField(default=False)
    has_phd = models.BooleanField(default=False)
    university = models.CharField(max_length=100)
    job_history = models.TextField(blank=True)
    academic_field = models.CharField(max_length=20, choices=FIELD_CHOICES)
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