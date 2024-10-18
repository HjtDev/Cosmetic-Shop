from django.shortcuts import render
from django.http.response import JsonResponse
from product.models import Product
from cart.models import Cart
import json


def add_cart_view(request):
    if request.method == 'POST':
        try:
            product = Product.visible_products.get(slug=request.POST.get('slug', None))
            quantity = request.POST.get('quantity', None)
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


def update_cart_view(request):
    if request.method == 'POST':
        try:
            # Load JSON data from request body
            data = json.loads(request.body)
            response = {'items': {}}
            cart = Cart(request)
            for item in data:
                slug = item.get('slug')
                product = Product.visible_products.get(slug=slug)
                quantity = item.get('quantity')
                if product is not None and quantity:
                    cart.update(product.id, quantity)
                    price = product.get_price()
                    response['items'][slug] = {'price': price, 'total': int(quantity) * price}
                    response['total_cost'] = cart.get_total_cost()
                else:
                    return JsonResponse({'error': 'Invalid Product or Quantity'})
            return JsonResponse(response)
        except Exception as e:
            print('Exception happened here', e)
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def cart_list_view(request):
    return render(request, 'product-cart.html')
