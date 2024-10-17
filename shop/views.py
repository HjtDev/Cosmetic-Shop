from django.shortcuts import render
from product.models import Product, Category
from jdatetime import datetime


def home_view(request):
    context = {
        'products': Product.visible_products.all().order_by('-sold')[:6],
        'today': datetime.now().date(),
        'categories': Category.objects.all()
    }
    return render(request, 'index.html', context)
