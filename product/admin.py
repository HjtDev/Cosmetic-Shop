from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from .models import Category, Product, Image, Feature, Comment


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    verbose_name = 'محصول'
    verbose_name_plural = 'محصولات'
    list_display = ('title', 'category', 'price', 'discount', 'inventory', 'is_visible')
    list_editable = ('price', 'discount', 'is_visible')
    search_fields = ('title', 'description', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = (
        ('last_sell', JDateFieldListFilter),
        ('created_at', JDateFieldListFilter),
        ('updated_at', JDateFieldListFilter),
        'category',
        'is_visible'
    )
    ordering = ('category', 'is_visible')

    inlines = [
        FeatureInline,
        ImageInline,
        CommentInline
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'big')
    list_filter = ('big',)
    list_editable = ('big',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'text', 'rating', 'is_visible')
    list_filter = (
        ('created_at', JDateFieldListFilter),
        ('updated_at', JDateFieldListFilter),
        'product',
        'user',
        'is_visible'
    )
    search_fields = ('text', 'rating')
    ordering = ('created_at', 'updated_at')
    list_editable = ('is_visible', 'rating')
