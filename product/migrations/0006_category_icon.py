# Generated by Django 5.1.2 on 2024-10-17 13:41

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_options_comment_is_visible_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=-1, scale=None, size=[80, 80], upload_to='category/icon', verbose_name='آیکون'),
        ),
    ]