# admin.py
from django.contrib import admin
from .models import CustomUser, Profile, Message

class ProfileInline(admin.StackedInline):
    model = Profile

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_expert', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # Add your custom fields here
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Message)