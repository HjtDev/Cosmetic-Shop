from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Comment


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
        'comments': product.comments.filter(is_visible=True),
        'related_products': Product.visible_products.exclude(id=product.id).filter(category=product.category).order_by('-updated_at')[:3]
    }
    return render(request, 'product-details.html', context)


def comment_view(request, slug):
    if request.method == 'POST':
        try:
            slug = request.POST.get('slug', None)
            if slug and request.user.is_authenticated:
                product = Product.visible_products.get(slug=slug)
                Comment.objects.create(
                    product=product,
                    user=request.user,
                    text=request.POST.get('text'),
                    rating=int(request.POST.get('rating'))
                )
                return JsonResponse({'message': 'نظر شما پس از تایید در سایت به نمایش در خواهد آمد.'})
            return JsonResponse({'message': 'شما ابتدا باید یک اکانت بسازید'})

        except:
            return JsonResponse({'error': 'Failed to like this product'})

    return JsonResponse({'error': 'Invalid request method'})
