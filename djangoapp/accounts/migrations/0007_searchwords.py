# Generated by Django 4.0.5 on 2022-07-03 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_home_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='search_words', to='accounts.home')),
            ],
        ),
    ]
