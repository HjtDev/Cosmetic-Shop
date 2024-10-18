from django.shortcuts import render
from django.http.response import JsonResponse
from product.models import Product
from cart.models import Cart


def add_view(request):
    if request.method == 'GET':
        try:
            product = Product.visible_products.get(slug=request.GET.get('slug', None))
            quantity = request.GET.get('quantity', None)
            if product is not None and quantity:
                cart = Cart(request)
                existed_in_cart = cart.add(product.id, quantity)
                context = {
                    'img': product.images.first().image.url,
                    'title': product.title,
                    'quantity': cart.cart['products'][str(product.id)]['quantity'],
                    'price': product.get_price(),
                    'slug': product.slug,
                }
                return JsonResponse({
                    'page': render(request, 'partials/cart_single_product.html', context).content.decode(),
                    'existed': existed_in_cart,
                    'total_price': cart.get_total_cost()
                })

            else:
                return JsonResponse({'error': 'Invalid Slug or Quantity'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def cart_list_view(request):
    return render(request, 'product-cart.html')
