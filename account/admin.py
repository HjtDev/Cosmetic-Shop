from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html
from django.contrib.auth.models import Group


admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ['phone']

    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = [
        'phone',
        'first_name',
        'last_name',
        'email',
        'is_active',
        'is_staff',
    ]

    fieldsets = (
        ('اصلی', {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email')}),
        ('دسترسی ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ ها', {'fields': ('last_login', 'date_joined')}),
        # ('Saved Products', {'fields': ['get_saved_products']}),
    )

    # readonly_fields = ['get_saved_products']

    # def get_saved_products(self, obj):
    #     product_links = [
    #         format_html('<a href="{}" target="_blank">{}</a>', product.get_absolute_url(), product.name)
    #         for product in obj.saved_products.all()
    #     ]
    #     return format_html(", ".join(product_links))  # Use format_html to
    #
    # get_saved_products.short_description = "Saved Products"

    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
