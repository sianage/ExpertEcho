# Generated by Django 4.2.4 on 2024-02-14 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Members', '0001_initial'),
        ('Debates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='debate',
            name='author_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_debates', to='Members.profile'),
        ),
        migrations.AddField(
            model_name='debate',
            name='opponent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='debate_opponent', to='Members.profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_comment', to='Members.profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='debate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Debates.debate'),
        ),
        migrations.AddIndex(
            model_name='debate',
            index=models.Index(fields=['created'], name='Debates_deb_created_78f5ab_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['created'], name='Debates_com_created_4d99ee_idx'),
        ),
    ]