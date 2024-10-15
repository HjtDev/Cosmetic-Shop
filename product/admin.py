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
    )
    ordering = ('category', 'is_visible')

    inlines = [
        FeatureInline,
        ImageInline,
        CommentInline
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
