from django.shortcuts import render, redirect


def checkout_view(request):
    if request.session.get('cart', None).get('products', None):
        return render(request, 'product-checkout.html')
    return redirect('cart:cart_list')
