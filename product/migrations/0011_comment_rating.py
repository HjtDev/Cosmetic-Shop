# Generated by Django 5.1.2 on 2024-10-19 16:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_category_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5)], verbose_name='امتیاز'),
        ),
    ]
