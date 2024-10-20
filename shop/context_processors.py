from jdatetime import datetime
from product.models import Product, Category
from django.db.models.aggregates import Sum


def today(request):
    return {'today': datetime.now().date()}


def header_products(request):
    products = Product.visible_products.all()
    return {
        'most_sold_products': products.order_by('-sold', '-updated_at')[:4],
        'new_products': products.order_by('-created_at', '-updated_at')[:4],
        'most_sold_categories': Category.objects.annotate(total_sold=Sum('products__sold'))
                                .filter(total_sold__isnull=False)
                                .order_by('-total_sold')[:4],
    }
