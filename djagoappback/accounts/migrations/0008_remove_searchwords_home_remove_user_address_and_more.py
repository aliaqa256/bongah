# Generated by Django 4.0.5 on 2022-07-03 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_searchwords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchwords',
            name='home',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='keywords',
        ),
        migrations.AddField(
            model_name='searchwords',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='search_words', to=settings.AUTH_USER_MODEL),
        ),
    ]
