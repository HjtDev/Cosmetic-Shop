from django.contrib import admin
from .models import Faq


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_visible')
    list_filter = ('is_visible',)
    list_editable = ('is_visible',)
    search_fields = ('question', 'answer')
