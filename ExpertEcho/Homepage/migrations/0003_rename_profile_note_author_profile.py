# Generated by Django 4.2.4 on 2024-04-24 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='profile',
            new_name='author_profile',
        ),
    ]
