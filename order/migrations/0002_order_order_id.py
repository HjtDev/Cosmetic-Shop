# Generated by Django 5.1.2 on 2024-10-15 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='', max_length=10, verbose_name='شماره سفارش'),
        ),
    ]
