# Generated by Django 4.0.6 on 2022-07-24 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_user_days_left'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='days',
            field=models.IntegerField(default=0),
        ),
    ]
