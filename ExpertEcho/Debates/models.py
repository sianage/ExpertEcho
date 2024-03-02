from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse

from Members.models import CustomUser, Profile
from fields import FIELD_CHOICES


class Debate(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=FIELD_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    author_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='authored_debates')
    opponent = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='debate_opponent')

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def save(self, *args, **kwargs):
        # Set category based on the academic_field of the author if not provided
        self.category = self.author_profile.academic_field
        super().save(*args, **kwargs)  # Call the superclass save method

    def __str__(self):
        author_name = "Unknown Author"

        if self.author_profile and hasattr(self.author_profile, 'user') and hasattr(self.author_profile.user,
                                                                                    'first_name'):
            author_name = self.author_profile.user.first_name

        return f'Debate: {self.title} by {author_name}'

    def get_absolute_url(self):
        # Define the URL to redirect to after successfully creating a debate
        return reverse('debate_detail', args=[str(self.id)])


class Comment(models.Model):
    debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #user
    commenter_name = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_comment')
    #form.media in view (tut 21)
    body = RichTextField(blank=True, null=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f'Comment by {self.body}'