from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Comment


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product-details.html', {'product': product})


def comment_view(request, slug):
    if request.method == 'POST':
        try:
            slug = request.POST.get('slug', None)
            if slug and request.user.is_authenticated:
                product = Product.visible_products.get(slug=slug)
                if not product.comments.filter(user=request.user).exists():
                    Comment.objects.create(
                        product=product,
                        user=request.user,
                        text=request.POST.get('text'),
                        rating=int(request.POST.get('rating'))
                    )
                    return JsonResponse({'message': 'نظر شما پس از تایید در سایت به نمایش در خواهد آمد.'})
                return JsonResponse({'message': 'شما قبلا برای این محصول نظر ثبت کرده اید.'})

        except:
            return JsonResponse({'error': 'Failed to like this product'})

    return JsonResponse({'error': 'Invalid request method'})


# def like_view(request):
#     if request.method == 'GET':
#         try:
#             slug = request.GET.get('slug')
#             if slug and request.user.is_authenticated:
#                 product = Product.visible_products.get(slug=slug)
#                 if not request.user in product.likes.all():
#                     product.likes.add(request.user)
#                     liked = True
#                 else:
#                     product.likes.remove(request.user)
#                     liked = False
#                 product.save()
#                 return JsonResponse({'liked': liked})
#             else:
#                 return JsonResponse({'user': True})
#         except:
#             return JsonResponse({'error': 'Failed to like this product'})
#     return JsonResponse({'error': 'Request method is invalid'})
