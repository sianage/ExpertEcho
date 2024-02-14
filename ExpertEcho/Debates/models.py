from ckeditor.fields import RichTextField
from django.db import models

from Members.models import CustomUser
from fields import FIELD_CHOICES


class Debate(models.Model):
    category = models.CharField(max_length=20, choices=FIELD_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='author')
    opponent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='opponent')
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def save(self, *args, **kwargs):
        # Set category based on the academic_field of the author
        self.category = self.author_profile.academic_field.capitalize()
        super().save(*args, **kwargs)  # Call the superclass save method

    def __str__(self):
        return f'Comment by {self.title}'

class Comment(models.Model):
    debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #user
    commenter_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #form.media in view (tut 21)
    body = RichTextField(blank=True, null=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f'Comment by {self.body}'