from django.db import models

class Debate(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="debates")
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author')
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='opponent')
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f'Comment by {self.title}'

class Comment(models.Model):
    debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #user
    commenter_name = models.ForeignKey(User, on_delete=models.CASCADE)
    #form.media in view (tut 21)
    body = RichTextField(blank=True, null=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f'Comment by {self.body}'