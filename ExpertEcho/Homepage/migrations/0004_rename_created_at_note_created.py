# Generated by Django 4.2.4 on 2024-04-24 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0003_rename_profile_note_author_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='created_at',
            new_name='created',
        ),
    ]