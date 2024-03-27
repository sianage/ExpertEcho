from django.contrib import admin

from .models import Debate, Comment

# Register your models here.
admin.site.register(Debate)
admin.site.register(Comment)