# Generated by Django 4.2.4 on 2024-02-14 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Blogs', '0001_initial'),
        ('Members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to='Members.profile'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-publish'], name='Blogs_post_publish_d95141_idx'),
        ),
    ]