from django.shortcuts import render, get_object_or_404
from .models import Product


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product-details.html', {'product': product})
