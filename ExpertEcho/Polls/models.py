from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model

from Members.models import Profile
from fields import FIELD_CHOICES
import Blogs.models



class Poll(models.Model):
    title = models.CharField(max_length=255)
    published = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=FIELD_CHOICES)
    author_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='polls')

    def save(self, *args, **kwargs):
        # Set category based on the academic_field of the author
        self.category = self.author_profile.academic_field
        super().save(*args, **kwargs)  # Call the superclass's save method

    @property
    def total_votes(self):
        return self.choice_set.aggregate(Sum('votes'))['votes__sum'] or 0



class Choice(models.Model):
    poll = models.ForeignKey(Poll, null=True, on_delete=models.CASCADE)
    choice = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def count_votes(self):
        return self.vote_set.count()

    def __str__(self):
        return self.choice

class Vote(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'choice']
