# Generated by Django 5.1.2 on 2024-10-15 08:46

import django.core.validators
import django.db.models.deletion
import django_jalali.db.models
import django_resized.forms
import jdatetime
import product.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='product_cat_name_4f76a1_idx')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('slug', models.SlugField(max_length=75, unique=True, verbose_name='اسلاگ')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='قیمت')),
                ('new_price', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='تخفیف به درصد')),
                ('inventory', models.PositiveIntegerField(verbose_name='موحودی در انبار')),
                ('sold', models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')),
                ('is_visible', models.BooleanField(default=True, verbose_name='نمایش در سایت')),
                ('last_sell', django_jalali.db.models.jDateTimeField(default=jdatetime.datetime.now, verbose_name='آخرین فروش')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین تغییر')),
                ('bought', models.ManyToManyField(blank=True, related_name='bought_products', to=settings.AUTH_USER_MODEL, verbose_name='کسانی که این محصول را خریده اند')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='product.category', verbose_name='دسته بندی')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_products', to=settings.AUTH_USER_MODEL, verbose_name='افرادی که این محصول را پسندیدند')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=30, verbose_name='نام')),
                ('value', models.CharField(blank=True, max_length=50, null=True, verbose_name='مقدار')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='product.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'ویژگی',
                'verbose_name_plural': 'ویژگی\u200cها',
                'ordering': ['key'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=-1, scale=None, size=[1920, 1080], upload_to=product.models.image_path, verbose_name='تصویر')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ آپلود')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصاویر',
                'ordering': ['created_at'],
                'indexes': [models.Index(fields=['product', 'created_at'], name='product_created_at_idx')],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=300, verbose_name='متن')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین تغییر')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='product.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'کامنت',
                'verbose_name_plural': 'کامنت ها',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['product'], name='comment_product_idx')],
            },
        ),
    ]
