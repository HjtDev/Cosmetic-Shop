from django.db import models
from account.models import User
from product.models import Product
from django_jalali.db import models as jmodels
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'در صف برسی', _('در صف برسی')  # Pending for review
        CONFIRMED = 'تایید سفارش', _('تایید سفارش')  # Order confirmed
        PREPARING = 'آماده سازی سفارش', _('آماده سازی سفارش')  # Preparing order
        DELIVERING = 'در حال ارسال', _('در حال ارسال')  # Delivered
        DONE = 'تکمیل شد', _('تکمیل شد')

    objects = jmodels.jManager()
    order_id = models.CharField(verbose_name='شماره سفارش', max_length=10, default='')
    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True,
                             verbose_name='کاربر')
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    email = models.EmailField(verbose_name='ایمیل', blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name='تلفن')
    address = models.CharField(max_length=300, verbose_name='آدرس')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    province = models.CharField(max_length=50, verbose_name='استان')
    city = models.CharField(max_length=50, verbose_name='شهر')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین تغییر')
    status = models.CharField(max_length=21, choices=OrderStatus.choices,
                              default=OrderStatus.PENDING, verbose_name='وضعیت')
    extra_description = models.TextField(verbose_name='توضیحات اضافه', max_length=300, default='', blank=True)
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'Order-{self.id}: {self.first_name} {self.last_name}'

    def get_items_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    get_items_cost.short_description = 'هزینه نهایی'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='سفارش')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='محصول')
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')

    def __str__(self):
        return f'OrderItem-{self.id}: {self.product}'

    def get_cost(self):
        return self.price * self.quantity

    get_cost.short_description = 'هزینه نهایی'


class Transaction(models.Model):
    class ReasonChoice(models.TextChoices):
        ORDER = 'برای سفارش', _('برای سفارش')
        REFUND = 'بازگشت وجه', _('بازگشت وجه')

    class TransactionStatusChoice(models.TextChoices):
        PAID = 'پرداخت موفق', _('پرداخت موفق')
        FAILED = 'پرداخت ناموفق', _('پرداخت ناموفق')

    objects = jmodels.jManager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='transactions', verbose_name='کاربر',
                             blank=True, null=True)
    reason = models.CharField(verbose_name='علت تراکنش', choices=ReasonChoice.choices, max_length=21)
    status = models.CharField(verbose_name='وضعیت تراکنش', choices=TransactionStatusChoice.choices, max_length=21)
    description = models.TextField(verbose_name='توضیحات نراکنش', max_length=100)
    price = models.PositiveIntegerField(verbose_name='هزینه', default=0)
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش ها'
        ordering = ('created_at',)

    def __str__(self):
        return f'سفارش شماره {self.id}'
