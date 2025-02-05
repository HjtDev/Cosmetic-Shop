from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels
from jdatetime import datetime
from django_resized import ResizedImageField
import os
from django.core.validators import MaxValueValidator
from account.models import User
from django.utils.text import slugify


class Category(models.Model):
    objects = jmodels.jManager()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    icon = ResizedImageField(verbose_name='آیکون', upload_to='category/icon', blank=True, null=True)
    big = models.BooleanField(verbose_name='دسته بندی بزرگ', default=False)
    updated_at = models.DateTimeField(verbose_name='آخرین تغییر', auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('product:category_view', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class VisibleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class Product(models.Model):
    objects = jmodels.jManager()
    title = models.CharField(verbose_name='عنوان', max_length=75)
    short_description = models.TextField(verbose_name='توضیحات کوتاه', max_length=200, blank=True, null=True)
    long_description = models.TextField(verbose_name='توضیحات بلند', blank=True, null=True)
    slug = models.CharField(verbose_name='اسلاگ', unique=True, max_length=75)
    price = models.PositiveIntegerField(verbose_name='قیمت', default=0)
    new_price = models.PositiveIntegerField(verbose_name='قیمت جدید', default=0)
    likes = models.ManyToManyField(User, related_name='liked_products', blank=True,
                                   verbose_name='افرادی که این محصول را پسندیدند')
    bought = models.ManyToManyField(User, related_name='bought_products', blank=True,
                                    verbose_name='کسانی که این محصول را خریده اند')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.DO_NOTHING,
                                 verbose_name='دسته بندی')
    inventory = models.PositiveIntegerField(verbose_name='موحودی در انبار', default=0)
    notify_me = models.ManyToManyField(User, related_name='notify_me', blank=True, verbose_name='به من اطلاع بده')
    sold = models.PositiveIntegerField(verbose_name='تعداد فروش', default=0)
    is_visible = models.BooleanField(verbose_name='نمایش در سایت', default=True)
    visible_products = VisibleManager()
    last_sell = jmodels.jDateTimeField(verbose_name='آخرین فروش', blank=True, null=True)
    created_at = jmodels.jDateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name='آخرین تغییر', auto_now=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['category', 'created_at'], name='product_idx')
        ]

    def get_price(self):
        return self.new_price if self.new_price else self.price

    def get_absolute_url(self):
        return reverse('product:detail_view', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        return super().save(*args, **kwargs)


def image_path(instance, filename):
    current_date = datetime.now()
    return f'product/{current_date.year}/{current_date.month}/{instance.product.slug}/{filename}'.replace(' ', '-')


class Image(models.Model):
    objects = jmodels.jManager()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='محصول')
    image = ResizedImageField(verbose_name='تصویر', upload_to=image_path)
    created_at = jmodels.jDateTimeField(verbose_name='تاریخ آپلود', auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['product', 'created_at'], name='product_created_at_idx')
        ]

    def delete(self, *args, **kwargs):
        os.remove(self.image.path)
        return super().delete(*args, **kwargs)


class Feature(models.Model):
    key = models.CharField(verbose_name='نام', max_length=30)
    value = models.CharField(verbose_name='مقدار', max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features', verbose_name='محصول')

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی‌ها'
        ordering = ['key']


class Comment(models.Model):
    objects = jmodels.jManager()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    text = models.TextField(verbose_name='متن', max_length=500)
    rating = models.PositiveIntegerField(verbose_name='امتیاز', validators=[MaxValueValidator(5)], default=1)
    is_visible = models.BooleanField(verbose_name='نمایش در سایت', default=False)

    created_at = jmodels.jDateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name='آخرین تغییر', auto_now=True)

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product'], name='comment_product_idx')
        ]

    def __str__(self):
        return f"{self.user.fullname()} commented on {self.product}"
