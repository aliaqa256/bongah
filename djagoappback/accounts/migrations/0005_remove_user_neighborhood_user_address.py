# Generated by Django 4.0.5 on 2022-07-02 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_apptokens'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='neighborhood',
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='address'),
        ),
    ]