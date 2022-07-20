# Generated by Django 4.0.6 on 2022-07-20 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_payments_is_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPayed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.TextField()),
                ('payment_id', models.TextField()),
                ('amount', models.IntegerField()),
                ('date', models.TextField(default='-')),
                ('card_number', models.TextField(default='****')),
                ('idpay_track_id', models.IntegerField(default=0)),
                ('bank_track_id', models.TextField(default=0)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
