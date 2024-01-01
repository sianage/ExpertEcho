from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from MainApp.models import Category

class Poll(models.Model):
    title = models.CharField(max_length=255)
    published = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="categories")

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'choice']