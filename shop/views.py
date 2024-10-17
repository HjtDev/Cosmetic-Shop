from django.shortcuts import render
from django.http.response import JsonResponse
from product.models import Product, Category
from jdatetime import datetime


def home_view(request):
    context = {
        'products': Product.visible_products.all().order_by('-sold')[:6],
        'today': datetime.now().date(),
        'categories': Category.objects.filter(big=False).order_by('-updated_at')[:12],
        'big_categories': Category.objects.filter(big=True).order_by('-updated_at')[:6]
    }
    return render(request, 'index.html', context)


def like_view(request):
    if request.method == 'GET':
        try:
            slug = request.GET.get('slug')
            if slug and request.user.is_authenticated:
                product = Product.visible_products.get(slug=slug)
                if not request.user in product.likes.all():
                    product.likes.add(request.user)
                    liked = True
                else:
                    product.likes.remove(request.user)
                    liked = False
                product.save()
                return JsonResponse({'liked': liked})
            else:
                return JsonResponse({'user': True})
        except:
            return JsonResponse({'error': 'Failed to like this product'})
    return JsonResponse({'error': 'Request method is invalid'})
