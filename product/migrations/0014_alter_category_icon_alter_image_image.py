# Generated by Django 5.1.2 on 2024-11-01 23:32

import django_resized.forms
import product.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_product_inventory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=100, scale=None, size=[1920, 1080], upload_to='category/icon', verbose_name='آیکون'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='PNG', keep_meta=True, quality=100, scale=None, size=[1920, 1080], upload_to=product.models.image_path, verbose_name='تصویر'),
        ),
    ]
