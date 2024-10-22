# Generated by Django 5.1.2 on 2024-10-17 14:04

import django_resized.forms
import product.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_category_icon_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=-1, scale=None, size=[80, 80], upload_to='category/icon', verbose_name='آیکون'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='PNG', keep_meta=True, quality=-1, scale=None, size=[1920, 1080], upload_to=product.models.image_path, verbose_name='تصویر'),
        ),
    ]
