from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, Comment, Category
from django.db.models import Q


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
        'comments': product.comments.filter(is_visible=True),
        'related_products': Product.visible_products.exclude(id=product.id).filter(category=product.category).order_by(
            '-updated_at')[:3]
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


def product_list_view(request):
    query = request.GET.get('query', None)
    if query:
        products = Product.visible_products.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(category__slug__icontains=query) |
            Q(slug__icontains=query)
        )
    else:
        products = Product.visible_products.all()

    context = {
        'products': products.order_by('-sold', '-created_at'),
        'title': 'تمامی محصولات' if not query else query,
        'categories': Category.objects.all(),
        'total_products': products.count()
    }
    return render(request, 'product-list.html', context)


def product_category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {
        'products': category.products.filter(is_visible=True),
        'title': category.name,
        'categories': Category.objects.all(),
        'total_products': Product.visible_products.count()
    }
    return render(request, 'product-list.html', context)
