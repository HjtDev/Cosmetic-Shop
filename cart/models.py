from django.db import models
from django.core.handlers.wsgi import WSGIRequest
from product.models import Product


class Cart:
    def __init__(self, request: WSGIRequest):
        self.cart = request.session
        if not self.cart.get('cart'):
            self.cart['cart'] = {}
        if not self.cart.get('products'):
            self.cart['products'] = {}  # Initialize products if not present

    def save(self):
        self.cart.modified = True

    def add(self, product_id, quantity):
        try:
            product = Product.visible_products.get(id=product_id)
            item = {'quantity': quantity, 'price': str(product.get_price())}
            self.cart['products'][str(product_id)] = item
            self.save()
        except Product.DoesNotExist:
            print('Tried to add a non-existing object to the cart')

    def remove(self, product_id):
        try:
            del self.cart['products'][str(product_id)]
            self.save()
        except KeyError:
            print('Failed to remove product from cart: Product does not exist in cart')

    def __iter__(self):
        # Fetch all products at once
        product_ids = list(self.cart.get('products', {}).keys())
        products = {product.id: product for product in Product.objects.filter(id__in=product_ids)}

        for product_id, item in self.cart.get('products', {}).items():
            product = products.get(int(product_id))  # Use int() for safety
            if product:  # Check if the product exists
                yield {
                    'product': product,
                    'quantity': item['quantity'],
                    'price': item['price'],
                }
            else:
                print(f'Product with id {product_id} does not exist.')

    def __len__(self):
        """Return the total number of items in the cart."""
        return sum(item['quantity'] for item in self.cart.get('products', {}).values())

    def clear(self):
        """Remove the cart from the session."""
        del self.cart['cart']
        self.save()
