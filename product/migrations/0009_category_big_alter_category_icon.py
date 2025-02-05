# Generated by Django 5.1.2 on 2024-10-17 18:16

import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_category_icon_alter_image_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='big',
            field=models.BooleanField(default=False, verbose_name='دسته بندی بزرگ'),
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=-1, scale=None, size=[1920, 1080], upload_to='category/icon', verbose_name='آیکون'),
        ),
    ]
