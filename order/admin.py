from django.contrib import admin
from .models import Order, OrderItem, Transaction
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1
    verbose_name = 'محصول'
    verbose_name_plural = 'محصولات'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'user',
        'phone',
        'province',
        'city',
        'created_at',
        'get_items_cost',
        'status',
        'paid',
    )
    list_filter = (
        'user',
        'status',
        'paid',
        ('created_at', JDateFieldListFilter),
        ('updated_at', JDateFieldListFilter)
    )
    search_fields = (
        'order_id',
        'first_name',
        'last_name',
        'email',
        'phone',
        'address',
        'postal_code',
        'province',
        'city',
    )
    list_editable = (
        'status',
        'paid'
    )
    ordering = ('created_at', 'updated_at')
    inlines = (OrderItemInline,)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'reason',
        'status',
        'description',
        'price',
        'created_at'
    )
    list_filter = (
        ('created_at', JDateFieldListFilter),
        'reason',
        'status'
    )
    search_fields = ('id',)
    ordering = ('created_at',)
