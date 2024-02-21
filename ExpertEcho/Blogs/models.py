from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from Members.models import CustomUser
from fields import FIELD_CHOICES
from Members.models import Profile

class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.DRAFT)
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

'''class Category(models.Model):
    category = models.CharField(max_length=255, choices=FIELD_CHOICES)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category

    #may need get_absolute_url function
    def get_absolute_url(self):
        return reverse('home', args=(str(self.id)))'''

class Post(models.Model):

    #Save posts as draft until ready to publish
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=255)
    #author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blog_posts')
    author_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blog_posts')
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    body = RichTextField(blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    #auto_now automatically updates the date when saving
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    #default manager
    objects = models.Manager()
    drafts = DraftManager()
    #custom manager
    published = PublishedManager()

    def save(self, *args, **kwargs):
        # Set category based on the academic_field of the author
        self.category = self.author_profile.academic_field.capitalize()
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        print("Author Profile User ID:", self.author_profile.user.id)

    #displays blog posts from newest to oldest
    class Meta:
        ordering = ['-publish']
        #DB index (speeds up data retrieval operations)
        indexes = [models.Index(fields=['-publish']),]

    def __str__(self):
        return f'{self.title} by {self.author_profile.first_name} {self.author_profile.last_name}'

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.id)))
