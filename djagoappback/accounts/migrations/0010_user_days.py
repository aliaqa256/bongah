# Generated by Django 4.0.6 on 2022-07-09 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_apptokens_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='days',
            field=models.IntegerField(blank=True, null=True, verbose_name='days'),
        ),
    ]
